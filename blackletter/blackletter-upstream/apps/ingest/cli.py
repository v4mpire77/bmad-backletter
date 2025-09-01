import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .adapters import ingest_file


def main():
    parser = argparse.ArgumentParser(description="Ingest contracts into chunks")
    parser.add_argument("--path", required=True, help="Path to folder with contracts")
    parser.add_argument("--out", required=True, help="Output JSONL file")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as outfile:
        for file_path in Path(args.path).glob("*"):
            if not file_path.is_file():
                continue
            contract_id = file_path.stem
            chunks = ingest_file(str(file_path), contract_id)
            for chunk in chunks:
                outfile.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
