from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import os

BASE_DIR = Path(__file__).resolve().parents[1]
RULES_DIR = BASE_DIR / "rules"


class RulepackError(RuntimeError):
    """Raised when a rulepack cannot be loaded or is invalid."""


@dataclass
class DetectorSpec:
    id: str
    type: str
    description: Optional[str] = None
    lexicon: Optional[str] = None


@dataclass
class Lexicon:
    name: str
    terms: List[str]


@dataclass
class Rulepack:
    name: str
    version: str
    detectors: List[DetectorSpec] = field(default_factory=list)
    lexicons: Dict[str, Lexicon] = field(default_factory=dict)


def _load_yaml_file(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class S3CompatibleStorage:
    """S3-compatible storage handler for rulepacks."""

    def __init__(self, endpoint_url: str = None, access_key: str = None, secret_key: str = None, bucket: str = None):
        self.endpoint_url = endpoint_url or os.getenv("S3_ENDPOINT_URL")
        self.access_key = access_key or os.getenv("S3_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("S3_SECRET_KEY")
        self.bucket = bucket or os.getenv("S3_BUCKET")
        self.enabled = bool(self.endpoint_url and self.access_key and self.secret_key and self.bucket)

    def get_rulepack(self, rulepack_file: str) -> Optional[Dict[str, Any]]:
        """Get rulepack from S3-compatible storage."""
        if not self.enabled:
            return None

        try:
            # Import boto3 only when needed to avoid dependency issues
            import boto3

            s3 = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )

            # Download the file content
            response = s3.get_object(Bucket=self.bucket, Key=rulepack_file)
            content = response['Body'].read().decode('utf-8')
            return yaml.safe_load(content) or {}
        except Exception as e:
            # Log error but don't fail - fallback to filesystem
            print(f"Warning: Failed to load rulepack from S3: {e}")
            return None


def api_rules_summary() -> Dict[str, Any]:
    rp = load_rulepack()
    if not rp:
        return {"packs": 0, "total_terms": 0, "by_pack": []}
    total_terms = sum(len(lx.terms) for lx in rp.lexicons.values())
    return {
        "packs": 1,
        "total_terms": total_terms,
        "by_pack": [
            {
                "id": rp.name,
                "version": rp.version,
                "hedging": total_terms,
                "discretionary": 0,
                "vague": 0,
                "regex": 0,
            }
        ],
    }


class RulepackLoader:
    def __init__(self, rules_dir: Path = RULES_DIR, rulepack_file: str = "art28_v1.yaml",
                 app_env: str = "dev", s3_storage: S3CompatibleStorage = None):
        self.rules_dir = rules_dir
        self.rulepack_file = rulepack_file
        self.app_env = app_env
        self.s3_storage = s3_storage or S3CompatibleStorage()
        self._cache: Optional[Rulepack] = None
        self._version_cache: Dict[str, List[Rulepack]] = {}

    def load(self) -> Rulepack:
        if self._cache:
            return self._cache

        # Try to load from S3 first if enabled
        data = None
        if self.s3_storage.enabled:
            data = self.s3_storage.get_rulepack(self.rulepack_file)

        # Fallback to filesystem
        if data is None:
            path = self.rules_dir / self.rulepack_file
            if not path.exists():
                raise RulepackError(f"rulepack file not found: {path}")
            data = _load_yaml_file(path)

        # Two formats supported:
        # 1) New schema with `meta` block validated by pydantic models
        # 2) Simple schema used by unit tests: {name, version, detectors, lexicons}
        use_meta_schema = isinstance(data, dict) and "meta" in data

        if use_meta_schema:
            # Validate the rulepack using our schema (lazy import to avoid pydantic import-time issues)
            try:
                from ..models.rulepack_schema import validate_rulepack, RulepackValidationError
                validated_rulepack = validate_rulepack(data)
            except RulepackValidationError as e:
                raise RulepackError(
                    f"Invalid rulepack schema: {e.message} (field: {e.field})"
                ) from e

            detectors = [
                DetectorSpec(
                    id=d.get("id"),
                    type="lexicon",  # default for meta schema detectors
                    description=None,
                    lexicon=None,
                )
                for d in (data.get("Detectors") or data.get("detectors") or [])
            ]
            if not detectors:
                raise RulepackError("missing detectors")

            lexicons: Dict[str, Lexicon] = {}
            # Load shared lexicon entries directly when provided
            shared = data.get("shared_lexicon", {}) or {}
            for key, value in shared.items():
                if isinstance(value, list):
                    lexicons[str(key)] = Lexicon(name=str(key), terms=[str(t) for t in value])

            rp = Rulepack(
                name=validated_rulepack.meta.pack_id,
                version=validated_rulepack.meta.version,
                detectors=detectors,
                lexicons=lexicons,
            )
        else:
            # Backwards-compatible simple schema
            detectors = [
                DetectorSpec(
                    id=d.get("id"),
                    type=d.get("type", "lexicon"),
                    description=d.get("description"),
                    lexicon=(d.get("lexicon") or "").rsplit(".", 1)[0] or None,
                )
                for d in data.get("detectors", [])
            ]
            if not detectors:
                raise RulepackError("missing detectors")

            lexicons: Dict[str, Lexicon] = {}
            for lx in data.get("lexicons", []):
                file = lx.get("file")
                if not file:
                    continue
                # Try to load from S3 first if enabled
                lex_data = None
                if self.s3_storage.enabled:
                    try:
                        lex_data = self.s3_storage.get_rulepack(f"lexicons/{file}")
                    except Exception:
                        lex_data = None

                # Fallback to filesystem
                if lex_data is None:
                    lex_data = _load_yaml_file(self.rules_dir / "lexicons" / file)

                name = (
                    lex_data.get("name")
                    or lex_data.get("lexicon_id")
                    or file.rsplit(".", 1)[0]
                )
                # Accept simple list or keyed list under e.g. 'hedges'
                terms_source = (
                    lex_data.get("terms")
                    or lex_data.get("hedges")
                    or []
                )
                terms = [str(t) for t in terms_source]
                lexicons[str(name).replace('-', '_')] = Lexicon(name=str(name), terms=terms)

            rp = Rulepack(
                name=str(data.get("name") or data.get("pack_id") or "unknown"),
                version=str(data.get("version") or "v0"),
                detectors=detectors,
                lexicons=lexicons,
            )
        self._cache = rp
        return rp

    def list_available_versions(self, pack_id: str) -> List[str]:
        """
        List all available versions of a rulepack.

        Args:
            pack_id: The rulepack ID to search for

        Returns:
            List of version strings in descending order (newest first)
        """
        versions = []

        # Check filesystem
        if self.rules_dir.exists():
            for file_path in self.rules_dir.glob(f"{pack_id}_v*.yaml"):
                # Extract version from filename (e.g., "art28_v1.2.3.yaml" -> "1.2.3")
                filename = file_path.stem
                if f"{pack_id}_v" in filename:
                    version_str = filename.replace(f"{pack_id}_v", "")
                    versions.append(version_str)

        # If S3 is enabled, also check there
        if self.s3_storage.enabled:
            try:
                import boto3
                s3 = boto3.client(
                    's3',
                    endpoint_url=self.s3_storage.endpoint_url,
                    aws_access_key_id=self.s3_storage.access_key,
                    aws_secret_access_key=self.s3_storage.secret_key,
                )

                # List objects with prefix
                response = s3.list_objects_v2(
                    Bucket=self.s3_storage.bucket,
                    Prefix=f"{pack_id}_v"
                )

                if 'Contents' in response:
                    for obj in response['Contents']:
                        filename = obj['Key']
                        if filename.endswith('.yaml'):
                            # Extract version from filename
                            stem = Path(filename).stem
                            if f"{pack_id}_v" in stem:
                                version_str = stem.replace(f"{pack_id}_v", "")
                                if version_str not in versions:
                                    versions.append(version_str)
            except Exception as e:
                print(f"Warning: Failed to list versions from S3: {e}")

        # Sort versions in descending order (newest first)
        versions.sort(key=lambda v: [int(x) for x in v.split('.')], reverse=True)
        return versions

    def load_version(self, pack_id: str, version: str) -> Rulepack:
        """
        Load a specific version of a rulepack.

        Args:
            pack_id: The rulepack ID
            version: The version to load

        Returns:
            Rulepack: The loaded rulepack
        """
        filename = f"{pack_id}_v{version}.yaml"
        original_file = self.rulepack_file
        self.rulepack_file = filename

        try:
            return self.load()
        finally:
            self.rulepack_file = original_file

    def get_latest_version(self, pack_id: str) -> Optional[str]:
        """
        Get the latest version of a rulepack.

        Args:
            pack_id: The rulepack ID

        Returns:
            The latest version string or None if no versions found
        """
        versions = self.list_available_versions(pack_id)
        return versions[0] if versions else None


def load_rulepack() -> Rulepack | None:
    try:
        return RulepackLoader().load()
    except RulepackError:
        return None


__all__ = [
    "RulepackError",
    "RulepackLoader",
    "Rulepack",
    "Lexicon",
    "DetectorSpec",
    "api_rules_summary",
    "load_rulepack",
    "S3CompatibleStorage",
]

# Backwards compatible aliases
Detector = DetectorSpec
