"""Phase 01: load raw HR files into LangChain Document objects.

Each file type gets its own LangChain loader. Nothing is merged:
- a PDF becomes one Document per page,
- a CSV becomes one Document per row,
- every other file becomes one Document.

Output: data/processed/loaded_documents.jsonl (one row = one Document).
"""

import json
from collections import Counter
from pathlib import Path

from langchain_community.document_loaders import (
    BSHTMLLoader,
    CSVLoader,
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "loaded_documents.jsonl"

# _source/ holds the Markdown the PDFs were generated from. Loading it too
# would index every policy twice, and only the PDFs carry page numbers.
SKIPPED_FOLDERS = {"_source"}
IGNORED_NAMES = {".DS_Store"}


def list_raw_files() -> list[Path]:
    """Return every raw HR file to load, skipping system files and _source/."""
    files = []
    for path in sorted(RAW_DIR.rglob("*")):
        if not path.is_file() or path.name in IGNORED_NAMES:
            continue
        folder = path.relative_to(RAW_DIR).parts[0]
        if folder in SKIPPED_FOLDERS:
            continue
        files.append(path)
    return files


def get_loader(path: Path):
    """Pick the LangChain loader for one file based on its extension."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(str(path))
    if ext == ".csv":
        return CSVLoader(str(path), encoding="utf-8")
    if ext == ".html":
        # A space between tags keeps table cells from running together.
        return BSHTMLLoader(str(path), open_encoding="utf-8", get_text_separator=" ")
    if ext == ".docx":
        return Docx2txtLoader(str(path))
    if ext in {".md", ".txt", ".json"}:
        return TextLoader(str(path), encoding="utf-8")
    return None


def add_simple_metadata(doc: Document, path: Path) -> Document:
    """Add normalized metadata on top of what the loader already set."""
    doc.metadata["source"] = path.relative_to(PROJECT_DIR).as_posix()
    doc.metadata["file_name"] = path.name
    doc.metadata["file_type"] = path.suffix.lower().lstrip(".")

    # PyPDFLoader stores a 0-based "page". Add a 1-based page for citations.
    if doc.metadata["file_type"] == "pdf" and "page" in doc.metadata:
        doc.metadata["page_number"] = doc.metadata["page"] + 1

    # CSVLoader stores a 0-based "row". Add a 1-based row for citations.
    if doc.metadata["file_type"] == "csv" and "row" in doc.metadata:
        doc.metadata["row_number"] = doc.metadata["row"] + 1

    return doc


def load_file(path: Path) -> list[Document]:
    """Load one file into a list of Documents with normalized metadata."""
    loader = get_loader(path)
    if loader is None:
        print(f"  Skipping unsupported file: {path.name}")
        return []
    docs = loader.load()
    return [add_simple_metadata(doc, path) for doc in docs]


def save_documents(docs: list[Document], output_file: Path) -> None:
    """Write one JSON line per Document: its text and its metadata."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for doc in docs:
            row = {"page_content": doc.page_content, "metadata": doc.metadata}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_documents(input_file: Path) -> list[Document]:
    """Read Documents back from a JSONL file written by save_documents."""
    docs = []
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs.append(Document(page_content=row["page_content"], metadata=row["metadata"]))
    return docs


def main() -> None:
    files = list_raw_files()
    print(f"Raw files to load: {len(files)} (skipping folders: {sorted(SKIPPED_FOLDERS)})\n")

    all_docs = []
    for path in files:
        all_docs.extend(load_file(path))

    save_documents(all_docs, OUTPUT_FILE)

    print(f"Document objects created: {len(all_docs)}\n")
    print("Documents per source file:")
    counts = Counter(doc.metadata["file_name"] for doc in all_docs)
    for file_name, count in counts.items():
        print(f"  {file_name:<42} {count}")

    # Preview the first PDF page, since PDFs carry page metadata.
    preview = next(doc for doc in all_docs if doc.metadata["file_type"] == "pdf")
    print("\nPreview of one Document:")
    print("-" * 60)
    print(preview.page_content[:400])
    print("-" * 60)
    print("Metadata:", json.dumps(preview.metadata, indent=2, ensure_ascii=False))
    print(f"\nSaved to: {OUTPUT_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
