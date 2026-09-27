"""Phase 05: store chunks, their embeddings and metadata in Chroma.

Rebuilding is predictable: the collection is deleted and recreated on every
run, so chunks are never duplicated.

Input:  data/processed/chunks.jsonl
Output: persistent Chroma database in data/chroma/
"""

import json
import sys
from pathlib import Path

import chromadb

from chunk_documents import read_chunks
from embeddings import EMBEDDING_MODEL_NAME, embed_texts

PROJECT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_DIR / "data" / "chroma"
COLLECTION_NAME = "hr_documents"
INSERT_BATCH_SIZE = 500

# How many candidates Chroma's HNSW search explores per query. The default
# (100) sometimes got stuck among the hundreds of near-identical CSV rows and
# missed the best policy chunks. Our collection is small (~1.7k chunks), so a
# wide search is cheap and makes results reliable.
HNSW_EF_SEARCH = 1000


def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection() -> chromadb.Collection:
    """Open the existing collection (used at question time)."""
    return get_chroma_client().get_collection(COLLECTION_NAME)


def recreate_collection(client: chromadb.PersistentClient) -> chromadb.Collection:
    """Delete the collection if it exists, then create an empty one."""
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        print(f"Collection '{COLLECTION_NAME}' already exists -> deleting it to rebuild from scratch.")
        client.delete_collection(COLLECTION_NAME)

    # We pass our own embeddings, so Chroma does not embed anything itself.
    return client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        configuration={"hnsw": {"space": "cosine", "ef_search": HNSW_EF_SEARCH}},
        metadata={"embedding_model": EMBEDDING_MODEL_NAME},
    )


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    chunks = read_chunks()
    print(f"Chunks to index: {len(chunks)}")

    print(f"Embedding chunks with {EMBEDDING_MODEL_NAME} ...")
    vectors = embed_texts([chunk.page_content for chunk in chunks])

    client = get_chroma_client()
    collection = recreate_collection(client)

    # Each record = chunk ID + chunk text + its embedding + its metadata.
    for start in range(0, len(chunks), INSERT_BATCH_SIZE):
        batch = chunks[start:start + INSERT_BATCH_SIZE]
        collection.add(
            ids=[chunk.metadata["chunk_id"] for chunk in batch],
            documents=[chunk.page_content for chunk in batch],
            embeddings=vectors[start:start + INSERT_BATCH_SIZE],
            metadatas=[chunk.metadata for chunk in batch],
        )

    final_count = collection.count()
    print(f"\nCollection name:         {COLLECTION_NAME}")
    print(f"Chunks inserted:         {len(chunks)}")
    print(f"Final number of records: {final_count}")
    assert final_count == len(chunks), "record count must match the number of chunks"

    sample_id = "leave-and-attendance-policy.pdf|page-6|chunk-0"
    sample = collection.get(ids=[sample_id], include=["metadatas", "documents"])
    print(f"\nOne stored record ({sample_id}):")
    print("  text:", sample["documents"][0][:120].replace("\n", " "), "...")
    print("  metadata:", json.dumps(sample["metadatas"][0], ensure_ascii=False))
    print(f"\nChroma persistence directory: {CHROMA_DIR.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
