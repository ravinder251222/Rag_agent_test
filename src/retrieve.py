"""Phase 06: embed a question and retrieve candidate chunks from Chroma.

    question -> same embedding model -> query vector -> Chroma search -> top_k chunks

No LLM is used here.

Usage:
    python src/retrieve.py "How many casual leaves do I get?"

Output: artifacts/retrieval_preview.json
"""

import json
import sys
from functools import lru_cache
from pathlib import Path

from build_index import get_collection
from embeddings import embed_query

TOP_K = 8

PROJECT_DIR = Path(__file__).resolve().parent.parent
PREVIEW_FILE = PROJECT_DIR / "artifacts" / "retrieval_preview.json"


@lru_cache(maxsize=1)
def load_collection():
    """Open the Chroma collection once and reuse it."""
    return get_collection()


def location_text(metadata: dict) -> str:
    """Readable location for a citation, e.g. 'page 6' or 'row 12'."""
    if "page_number" in metadata:
        return f"page {metadata['page_number']}"
    if "row_number" in metadata:
        return f"row {metadata['row_number']}"
    return ""


def retrieve(question: str, top_k: int = TOP_K) -> list[dict]:
    """Return the top_k most similar chunks, best first."""
    query_vector = embed_query(question)
    results = load_collection().query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    candidates = []
    for rank, (chunk_id, text, metadata, distance) in enumerate(zip(
        results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0],
    ), start=1):
        candidates.append({
            "retrieval_rank": rank,
            "chunk_id": chunk_id,
            "source": metadata["source"],
            "file_name": metadata["file_name"],
            "page": metadata.get("page_number"),
            "location": location_text(metadata),
            # Cosine distance: 0 = identical direction. Similarity = 1 - distance.
            "distance": round(distance, 4),
            "similarity": round(1 - distance, 4),
            "text": text,
            "metadata": metadata,
        })
    return candidates


def save_retrieval_preview(question: str, candidates: list[dict]) -> None:
    PREVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    rows = [{k: v for k, v in c.items() if k != "metadata"} for c in candidates]
    output = {"question": question, "top_k": len(candidates), "candidates": rows}
    PREVIEW_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")


def print_candidates(candidates: list[dict]) -> None:
    for c in candidates:
        where = f"{c['file_name']} {c['location']}".strip()
        print(f"\n#{c['retrieval_rank']}  similarity {c['similarity']:.3f}  {where}")
        print(f"    {c['text'][:200].replace(chr(10), ' ')} ...")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    question = " ".join(sys.argv[1:]) or input("Ask an HR question: ")
    candidates = retrieve(question)

    print(f"Question: {question}")
    print(f"Top {len(candidates)} candidates from Chroma (no LLM used):")
    print_candidates(candidates)

    save_retrieval_preview(question, candidates)
    print(f"\nSaved to: {PREVIEW_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
