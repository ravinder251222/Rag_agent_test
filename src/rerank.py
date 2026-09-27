"""Phase 07: rerank the retrieved candidates with a cross-encoder.

Retrieval quickly creates a shortlist. Reranking looks at the question and
each shortlisted chunk more carefully and chooses the strongest context.

    8 retrieved candidates -> cross-encoder scores (question, chunk) -> best 4

This is a separate step from Chroma retrieval. No LLM is used here.

Usage:
    python src/rerank.py "How many casual leaves do I get?"

Output: artifacts/reranked_preview.json
"""

import json
import sys
from functools import lru_cache
from pathlib import Path

from sentence_transformers import CrossEncoder

from retrieve import retrieve, save_retrieval_preview

RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
TOP_N = 4

PROJECT_DIR = Path(__file__).resolve().parent.parent
PREVIEW_FILE = PROJECT_DIR / "artifacts" / "reranked_preview.json"


@lru_cache(maxsize=1)
def load_reranker() -> CrossEncoder:
    """Load the cross-encoder once and reuse it."""
    return CrossEncoder(RERANKER_MODEL_NAME)


def rerank(question: str, candidates: list[dict], top_n: int = TOP_N) -> list[dict]:
    """Score every (question, chunk text) pair and keep the best top_n."""
    pairs = [(question, c["text"]) for c in candidates]
    scores = load_reranker().predict(pairs)

    scored = []
    for candidate, score in zip(candidates, scores):
        scored.append({**candidate, "rerank_score": round(float(score), 4)})

    scored.sort(key=lambda c: c["rerank_score"], reverse=True)
    for new_rank, candidate in enumerate(scored, start=1):
        candidate["rerank_rank"] = new_rank
    return scored[:top_n]


def save_rerank_preview(question: str, candidates: list[dict], best: list[dict]) -> None:
    PREVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    fields = ["retrieval_rank", "rerank_rank", "rerank_score", "similarity",
              "chunk_id", "source", "file_name", "page", "location", "text"]
    output = {
        "question": question,
        "reranker_model": RERANKER_MODEL_NAME,
        "retrieved_count": len(candidates),
        "kept_top_n": len(best),
        "reranked_chunks": [{field: c[field] for field in fields} for c in best],
    }
    PREVIEW_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    question = " ".join(sys.argv[1:]) or input("Ask an HR question: ")
    candidates = retrieve(question)
    save_retrieval_preview(question, candidates)
    best = rerank(question, candidates)
    save_rerank_preview(question, candidates, best)

    print(f"Question: {question}\n")
    print("Original retrieval order (Chroma, fast vector similarity):")
    for c in candidates:
        print(f"  #{c['retrieval_rank']}  sim {c['similarity']:.3f}  {c['chunk_id']}")

    print(f"\nReranked order (cross-encoder, kept best {len(best)}):")
    for c in best:
        print(f"  #{c['rerank_rank']}  score {c['rerank_score']:>7.3f}  (was #{c['retrieval_rank']})  {c['chunk_id']}")
        print(f"        {c['text'][:160].replace(chr(10), ' ')} ...")

    print(f"\nSaved to: {PREVIEW_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
