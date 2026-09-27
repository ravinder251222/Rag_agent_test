"""Phase 04: turn chunk text into embedding vectors.

The SAME model and the SAME function are used for document chunks (at
indexing time) and for user questions (at query time), so both live in the
same vector space.

One chunk -> one 384-number vector. Embedding a batch of N chunks returns
N vectors, one per chunk, in the same order.

Output: artifacts/embedding_preview.json
"""

import json
import sys
from functools import lru_cache
from pathlib import Path

from sentence_transformers import SentenceTransformer

from chunk_documents import read_chunks

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L12-v2"
PREVIEW_CHUNKS = 5

PROJECT_DIR = Path(__file__).resolve().parent.parent
PREVIEW_FILE = PROJECT_DIR / "artifacts" / "embedding_preview.json"


@lru_cache(maxsize=1)
def load_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts. Returns exactly one vector per input text.

    Vectors are normalized to length 1, so cosine similarity is a simple
    dot product.
    """
    model = load_embedding_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=len(texts) > 100)
    return vectors.tolist()


def embed_query(question: str) -> list[float]:
    """Embed one user question with the same model used for the chunks."""
    return embed_texts([question])[0]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    chunks = read_chunks()
    print(f"Chunks read: {len(chunks)}")
    print(f"Embedding model: {EMBEDDING_MODEL_NAME}\n")

    # Embed a small batch: several chunks go in, one vector per chunk comes out.
    batch = chunks[:PREVIEW_CHUNKS]
    vectors = embed_texts([chunk.page_content for chunk in batch])
    assert len(vectors) == len(batch), "each chunk must get exactly one vector"

    dimension = len(vectors[0])
    print(f"Batch of {len(batch)} chunks -> {len(vectors)} vectors, each with {dimension} numbers:")
    preview = []
    for chunk, vector in zip(batch, vectors):
        chunk_id = chunk.metadata["chunk_id"]
        print(f"  {chunk_id:<45} -> {len(vector)}-number vector {[round(x, 4) for x in vector[:4]]} ...")
        preview.append({
            "chunk_id": chunk_id,
            "text_preview": chunk.page_content[:150],
            "vector_dimension": len(vector),
            "first_10_numbers": [round(x, 6) for x in vector[:10]],
        })

    # Embed every chunk to confirm the whole set works (Phase 05 stores them).
    all_vectors = embed_texts([chunk.page_content for chunk in chunks])
    assert len(all_vectors) == len(chunks)
    assert all(len(vector) == dimension for vector in all_vectors)
    print(f"\nAll {len(chunks)} chunks embedded -> {len(all_vectors)} vectors, all {dimension}-dimensional.")

    # A question goes through the same model and lands in the same space.
    question_vector = embed_query("How many casual leaves do I get?")
    print(f"A question also becomes one {len(question_vector)}-number vector.")

    PREVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "embedding_model": EMBEDDING_MODEL_NAME,
        "vector_dimension": dimension,
        "total_chunks": len(chunks),
        "total_vectors": len(all_vectors),
        "preview": preview,
    }
    PREVIEW_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved to: {PREVIEW_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
