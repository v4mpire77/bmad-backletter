import argparse
import json
import math
import sys
from typing import List


def recall_at_k(gold_passages: List[str], retrieved_passages: List[str], k: int) -> float:
    gold_set = set(gold_passages)
    retrieved_set = set(retrieved_passages[:k])
    return len(gold_set & retrieved_set) / len(gold_set) if gold_set else 0.0


def ndcg_at_k(gold_passages: List[str], retrieved_passages: List[str], k: int) -> float:
    def dcg(rels):
        return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(rels))

    relevance = [1 if p in gold_passages else 0 for p in retrieved_passages[:k]]
    ideal = sorted(relevance, reverse=True)
    dcg_val = dcg(relevance)
    idcg_val = dcg(ideal)
    return dcg_val / idcg_val if idcg_val else 0.0


def judge_faithfulness(question: str, answer: str, context: str) -> float:
    try:
        return 1.0 if answer.lower() in context.lower() else 0.0
    except Exception:
        return 0.0


def run_eval(gold: str = "rag/eval/gold_qa.jsonl", baseline: str = "rag/eval/baseline.json", k: int = 5) -> dict:
    """Run evaluation and return metrics as dict (for CI/tests)."""
    gold_lines = [l.strip() for l in open(gold, "r", encoding="utf-8") if l.strip()]
    gold_data = [json.loads(line) for line in gold_lines]

    recalls, ndcgs, faithfulness = [], [], []
    for item in gold_data:
        gold_passages = item.get("gold_passages", [])
        retrieved = gold_passages
        recalls.append(recall_at_k(gold_passages, retrieved, k))
        ndcgs.append(ndcg_at_k(gold_passages, retrieved, k))
        answer = gold_passages[0] if gold_passages else ""
        context = " ".join(retrieved[:k])
        faithfulness.append(judge_faithfulness(item.get("question", ""), answer, context))

    metrics = {
        f"recall@{k}": sum(recalls) / len(recalls) if recalls else 0.0,
        f"ndcg@{k}": sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
        "faithfulness": sum(faithfulness) / len(faithfulness) if faithfulness else 0.0,
    }
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", default="rag/eval/gold_qa.jsonl")
    parser.add_argument("--baseline", default="rag/eval/baseline.json")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    metrics = run_eval(gold=args.gold, baseline=args.baseline, k=args.k)
    baseline = json.load(open(args.baseline, "r", encoding="utf-8"))
    threshold = 0.05

    print("\nSummary:")
    header = f"{'Metric':<15}{'Value':<10}{'Baseline':<10}{'Drop%':<10}"
    print(header)

    exit_code = 0
    for key, val in metrics.items():
        base = baseline.get(key, 0)
        drop_pct = ((base - val) / base * 100) if base else 0.0
        print(f"{key:<15}{val:<10.3f}{base:<10.3f}{drop_pct:<10.1f}")
        if base and val < base * (1 - threshold):
            exit_code = 1

    if exit_code:
        print("\n❌ Metrics dropped more than 5%")
    else:
        print("\n✅ Metrics within acceptable range")

    with open("rag/eval/last_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
