"""Phase 03: split cleaned Documents into smaller chunks.

Each chunk keeps the metadata of its parent Document and gets:
- chunk_index: position of the chunk inside its parent Document (0-based),
- chunk_id:    a readable unique ID such as
               "leave-and-attendance-policy.pdf|page-6|chunk-0".

Input:  data/processed/cleaned_documents.jsonl
Output: data/processed/chunks.jsonl (one row = one chunk)
"""

import json
import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from load_documents import read_documents, save_documents

CHUNK_SIZE = 800  # characters
CHUNK_OVERLAP = 120  # characters

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "cleaned_documents.jsonl"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "chunks.jsonl"


def location_label(metadata: dict) -> str:
    """Return the page (PDF) or row (CSV) part of a chunk ID, if any."""
    if "page_number" in metadata:
        return f"page-{metadata['page_number']}"
    if "row_number" in metadata:
        return f"row-{metadata['row_number']}"
    return ""


def make_chunk_id(metadata: dict, chunk_index: int) -> str:
    parts = [metadata["file_name"], location_label(metadata), f"chunk-{chunk_index}"]
    return "|".join(part for part in parts if part)


def chunk_documents(docs: list[Document]) -> list[Document]:
    """Split each Document separately so chunks never mix two sources."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    chunks = []
    for doc in docs:
        if not doc.page_content.strip():
            continue
        pieces = splitter.split_text(doc.page_content)
        for chunk_index, piece in enumerate(pieces):
            metadata = dict(doc.metadata)
            metadata["chunk_index"] = chunk_index
            metadata["chunk_id"] = make_chunk_id(metadata, chunk_index)
            chunks.append(Document(page_content=piece, metadata=metadata))
    return chunks


def read_chunks(input_file: Path = OUTPUT_FILE) -> list[Document]:
    return read_documents(input_file)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    docs = read_documents(INPUT_FILE)
    chunks = chunk_documents(docs)
    save_documents(chunks, OUTPUT_FILE)

    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    assert len(ids) == len(set(ids)), "chunk_id values must be unique"

    print(f"Chunk size / overlap:     {CHUNK_SIZE} / {CHUNK_OVERLAP} characters")
    print(f"Cleaned Document objects: {len(docs)}")
    print(f"Chunks created:           {len(chunks)}")
    lengths = [len(chunk.page_content) for chunk in chunks]
    print(f"Chunk length min/avg/max: {min(lengths)} / {sum(lengths) // len(lengths)} / {max(lengths)}")

    # Preview the first chunks of one PDF so page metadata is visible.
    preview = [c for c in chunks if c.metadata["file_name"] == "leave-and-attendance-policy.pdf"][:3]
    for chunk in preview:
        print("\n" + "=" * 60)
        print(f"chunk_id: {chunk.metadata['chunk_id']}   length: {len(chunk.page_content)} chars")
        print("-" * 60)
        print(chunk.page_content)
        print("-" * 60)
        print("metadata:", json.dumps(chunk.metadata, ensure_ascii=False))

    print(f"\nSaved to: {OUTPUT_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
