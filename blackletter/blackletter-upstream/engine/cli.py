import argparse
import json
from pathlib import Path
from typing import List, Dict, Any

from .rules import load_rules
from .executors import execute_rules


def load_chunks(path: str) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            chunks.append(json.loads(line))
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description='Compliance checker')
    parser.add_argument('--chunks', required=True, help='Path to chunks JSONL file')
    parser.add_argument('--rules', required=True, help='Path to rules YAML file')
    parser.add_argument('--out', required=True, help='Where to write findings JSON')
    args = parser.parse_args()

    rules = load_rules(args.rules)
    chunks = load_chunks(args.chunks)
    findings = execute_rules(rules, chunks)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2)

    print(f"Wrote {len(findings)} findings to {args.out}")


if __name__ == '__main__':
    main()
