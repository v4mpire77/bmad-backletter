"""CLI wrapper for running RAG evaluation."""

import argparse
from rag.eval import evaluate


def main() -> None:
    """Parse arguments and forward them to the evaluation logic."""

    parser = argparse.ArgumentParser(description="Run RAG evaluation")
    parser.add_argument(
        "--gold", default="rag/eval/gold_qa.jsonl", help="Path to gold QA file"
    )
    parser.add_argument(
        "--baseline", default="rag/eval/baseline.json", help="Baseline metrics"
    )
    parser.add_argument("-k", type=int, default=5, help="Number of passages")
    args = parser.parse_args()

    metrics = evaluate.run_eval(gold=args.gold, baseline=args.baseline, k=args.k)
    print(metrics)


if __name__ == "__main__":
    main()

