import json
import math


def recall_at_k(gold_passages, retrieved_passages, k):
    gold_set = set(gold_passages)
    retrieved_set = set(retrieved_passages[:k])
    return len(gold_set & retrieved_set) / len(gold_set) if gold_set else 0.0


def ndcg_at_k(gold_passages, retrieved_passages, k):
    def dcg(rels):
        return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(rels))
    relevance = [1 if p in gold_passages else 0 for p in retrieved_passages[:k]]
    ideal = sorted(relevance, reverse=True)
    dcg_val = dcg(relevance)
    idcg_val = dcg(ideal)
    return dcg_val / idcg_val if idcg_val else 0.0


def main():
    k = 5
    gold = [json.loads(line) for line in open('rag/eval/gold_qa.jsonl', 'r', encoding='utf-8')]
    baseline = json.load(open('rag/eval/baseline.json', 'r', encoding='utf-8'))

    recalls, ndcgs, faiths = [], [], []
    for item in gold:
        question = item['question']
        gold_passages = item.get('gold_passages', [])
        retrieved = gold_passages
        r = recall_at_k(gold_passages, retrieved, k)
        n = ndcg_at_k(gold_passages, retrieved, k)
        a = gold_passages[0] if gold_passages else ''
        context = ' '.join(retrieved[:k])
        f = 1.0 if a.lower() in context.lower() else 0.0
        recalls.append(r)
        ndcgs.append(n)
        faiths.append(f)
        print(f"question={question}\n  recall={r}, ndcg={n}, faith={f}\n")

    metrics = {
        f"recall@{k}": sum(recalls)/len(recalls) if recalls else 0.0,
        f"ndcg@{k}": sum(ndcgs)/len(ndcgs) if ndcgs else 0.0,
        'faithfulness': sum(faiths)/len(faiths) if faiths else 0.0
    }
    print('computed metrics:', json.dumps(metrics, indent=2))
    print('baseline:', json.dumps(baseline, indent=2))
    threshold = 0.05
    for key, val in metrics.items():
        base = baseline.get(key, 0)
        print(f"compare {key}: val={val}, base={base}")
        if base and val < base * (1 - threshold):
            print(f"  DROPPED: {key} below threshold")

if __name__ == '__main__':
    main()
