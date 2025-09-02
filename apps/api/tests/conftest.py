import importlib.util
import sys
import types

import pytest


def _has_pkg(name: str) -> bool:
    return importlib.util.find_spec(name) is not None

boto3_missing = not _has_pkg("boto3")


@pytest.fixture
def fake_boto3_client(monkeypatch):
    """Patch boto3.client globally for modules that import boto3 internally."""
    if boto3_missing:
        pytest.skip("boto3 not installed; skipping S3-dependent tests")

    import boto3

    class _FakeS3:
        def get_object(self, Bucket, Key):
            class _Body:
                def read(self):
                    return b"{}"
            return {"Body": _Body()}

    def _fake_client(name, *args, **kwargs):
        if name == "s3":
            return _FakeS3()
        return boto3.client(name, *args, **kwargs)

    monkeypatch.setattr("boto3.client", _fake_client, raising=True)


OPTIONAL_PKGS = ("docx2python", "blingfire", "fitz")


def _ensure_stub(name: str):
    if name in sys.modules:
        return
    m = types.ModuleType(name)
    if name == "docx2python":
        def docx2python(path, *a, **k):
            class _D:
                text = ""
            return _D()
        m.docx2python = docx2python
    elif name == "blingfire":
        def text_to_sentences(s: str) -> str:
            return s
        m.text_to_sentences = text_to_sentences
    elif name == "fitz":
        class _Doc:
            def __init__(self, *a, **k):
                pass
        m.Document = _Doc
    sys.modules[name] = m


@pytest.fixture(autouse=True, scope="session")
def guard_optional_deps():
    """Stub out optional heavy deps if they are missing."""
    for name in OPTIONAL_PKGS:
        if not _has_pkg(name):
            _ensure_stub(name)

