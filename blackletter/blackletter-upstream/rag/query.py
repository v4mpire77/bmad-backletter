import os
import json
from typing import List, Dict, Optional

try:
    import chromadb
except Exception:  # pragma: no cover - chromadb optional for linting
    chromadb = None  # type: ignore

RRF_K = 60


def _query_collection(db_path: str, collection_name: str, query: str, n_results: int,
                      filters: Optional[Dict[str, str]] = None) -> List[Dict]:
    """Query a ChromaDB collection and return ranked documents.

    If the store or collection is missing, an empty list is returned so that
    callers can handle environments without the vector data present.
    """
    if chromadb is None or n_results <= 0:
        return []

    try:
        client = chromadb.PersistentClient(path=db_path)
        collection = client.get_collection(collection_name)
        kwargs: Dict = {"query_texts": [query], "n_results": n_results}
        if filters:
            kwargs["where"] = filters
        results = collection.query(**kwargs)
    except Exception:
        return []

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    output = []
    for rank, (doc, meta, id_) in enumerate(zip(docs, metas, ids), start=1):
        meta = meta or {}
        output.append({
            "id": id_,
            "text": doc,
            "source": meta.get("source", id_),
            "page": meta.get("page"),
            "section": meta.get("section"),
            "url": meta.get("url"),
            "rank": rank,
        })
    return output


def _rrf(result_sets: List[List[Dict]], top_k: int) -> List[Dict]:
    """Fuse rankings using reciprocal rank fusion and deduplicate by source."""
    scores: Dict[str, float] = {}
    best_meta: Dict[str, Dict] = {}

    for results in result_sets:
        for item in results:
            key = item["source"]
            score = 1.0 / (RRF_K + item["rank"])
            scores[key] = scores.get(key, 0.0) + score
            if key not in best_meta or item["rank"] < best_meta[key]["rank"]:
                best_meta[key] = item

    fused = []
    for key, score in scores.items():
        meta = best_meta[key]
        fused.append({
            "source": key,
            "text": meta.get("text"),
            "score": score,
            "page": meta.get("page"),
            "section": meta.get("section"),
            "url": meta.get("url"),
        })

    fused.sort(key=lambda x: x["score"], reverse=True)
    return fused[:top_k]


def retrieve(query: str, k_contracts: int = 4, k_authority: int = 6,
             contract_id: Optional[str] = None, ruleset: Optional[str] = None,
             severity: Optional[str] = None) -> Dict:
    """Retrieve contexts for a query from contract and authority stores.

    Parameters
    ----------
    query: str
        Natural language question.
    k_contracts: int
        Number of contract contexts to retrieve.
    k_authority: int
        Number of authority contexts to retrieve.
    contract_id, ruleset, severity: Optional[str]
        Filters applied to the underlying vector stores.

    Returns
    -------
    dict
        ``{"query": query, "results": [...]}`` where each result contains
        ``text``, ``score``, ``page``, ``section`` and ``url``.
    """
    filters = {}
    if contract_id:
        filters["contract_id"] = contract_id
    if ruleset:
        filters["ruleset"] = ruleset
    if severity:
        filters["severity"] = severity

    contracts_path = os.getenv("CONTRACTS_DB_PATH", "data/contracts")
    contracts_collection = os.getenv("CONTRACTS_COLLECTION", "contracts")
    authority_path = os.getenv("AUTHORITY_DB_PATH", "data/authority")
    authority_collection = os.getenv("AUTHORITY_COLLECTION", "authority")

    contract_results = _query_collection(contracts_path, contracts_collection,
                                         query, k_contracts, filters)
    authority_results = _query_collection(authority_path, authority_collection,
                                          query, k_authority, filters)

    fused = _rrf([contract_results, authority_results], k_contracts + k_authority)
    return {"query": query, "results": fused}


if __name__ == "__main__":  # pragma: no cover - manual use
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(json.dumps(retrieve(q), indent=2))
