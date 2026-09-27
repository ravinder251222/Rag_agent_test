"""Phase 02: conservatively clean the loaded Documents.

Only whitespace and clearly repeated boilerplate are touched:
- non-breaking spaces become normal spaces,
- runs of spaces inside a line become one space,
- lines are trimmed (except JSON, where indentation shows structure),
- 3+ blank lines become one blank line,
- running headers/footers repeated on most pages of a PDF are removed,
- navigation/footer lines repeated on most HTML pages are removed,
- standalone "Page N" lines in PDFs are removed (page_number stays in metadata),
- table-of-contents dot leaders (". . . . .") become "...".

Sentences are never rewritten or summarized, and metadata is kept unchanged.

Input:  data/processed/loaded_documents.jsonl
Output: data/processed/cleaned_documents.jsonl
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from langchain_core.documents import Document

from load_documents import read_documents, save_documents

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_DIR / "data" / "processed" / "loaded_documents.jsonl"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "cleaned_documents.jsonl"

# A line counts as boilerplate only if it appears on at least this share of
# the pages in its group, and the group has at least this many pages.
BOILERPLATE_MIN_SHARE = 0.8
BOILERPLATE_MIN_GROUP_SIZE = 3

PAGE_NUMBER_LINE = re.compile(r"^Page \d+$")
NBSP = chr(0xA0)  # non-breaking space
DOT_LEADER = re.compile(r"(?:\. ?){4,}")


def boilerplate_group(doc: Document) -> str | None:
    """Return the group a Document is compared against for repeated lines.

    Pages of the same PDF form one group. All HTML pages form one group
    (they share the intranet navigation and footer). Other files have no group.
    """
    file_type = doc.metadata["file_type"]
    if file_type == "pdf":
        return doc.metadata["file_name"]
    if file_type == "html":
        return "html pages"
    return None


def find_boilerplate_lines(docs: list[Document]) -> dict[str, set[str]]:
    """Find lines repeated on most Documents of each group."""
    groups = defaultdict(list)
    for doc in docs:
        group = boilerplate_group(doc)
        if group:
            groups[group].append(doc)

    boilerplate = {}
    for group, group_docs in groups.items():
        if len(group_docs) < BOILERPLATE_MIN_GROUP_SIZE:
            continue
        line_counts = Counter()
        for doc in group_docs:
            unique_lines = {line.strip() for line in doc.page_content.splitlines() if line.strip()}
            line_counts.update(unique_lines)
        min_count = BOILERPLATE_MIN_SHARE * len(group_docs)
        boilerplate[group] = {line for line, count in line_counts.items() if count >= min_count}
    return boilerplate


def clean_text(text: str, file_type: str, boilerplate_lines: set[str]) -> str:
    """Apply the conservative cleaning rules to one Document's text."""
    text = text.replace(NBSP, " ").replace("\r\n", "\n")

    cleaned_lines = []
    for line in text.splitlines():
        if line.strip() in boilerplate_lines:
            continue
        if file_type == "pdf" and PAGE_NUMBER_LINE.match(line.strip()):
            continue

        if file_type == "json":
            # Keep indentation; only collapse spaces after the first character.
            line = re.sub(r"(?<=\S) {2,}", " ", line.rstrip())
        else:
            line = re.sub(r"[ \t]+", " ", line).strip()
            line = DOT_LEADER.sub("... ", line).strip()
        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_documents(docs: list[Document]) -> tuple[list[Document], dict[str, set[str]]]:
    """Clean every Document. Metadata is copied over unchanged."""
    boilerplate = find_boilerplate_lines(docs)
    cleaned = []
    for doc in docs:
        lines_to_remove = boilerplate.get(boilerplate_group(doc), set())
        text = clean_text(doc.page_content, doc.metadata["file_type"], lines_to_remove)
        cleaned.append(Document(page_content=text, metadata=dict(doc.metadata)))
    return cleaned, boilerplate


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    loaded = read_documents(INPUT_FILE)
    cleaned, boilerplate = clean_documents(loaded)
    save_documents(cleaned, OUTPUT_FILE)

    print(f"Documents read:    {len(loaded)}")
    print(f"Documents written: {len(cleaned)} (same count, same metadata)\n")

    print("Repeated boilerplate lines removed:")
    for group, lines in boilerplate.items():
        print(f"  {group}: {len(lines)} lines, e.g. {sorted(lines)[:3]}")

    print("\nCharacters before -> after, by file type:")
    totals = defaultdict(lambda: [0, 0])
    for before, after in zip(loaded, cleaned):
        totals[before.metadata["file_type"]][0] += len(before.page_content)
        totals[before.metadata["file_type"]][1] += len(after.page_content)
    for file_type, (before_chars, after_chars) in sorted(totals.items()):
        print(f"  {file_type:<5} {before_chars:>9,} -> {after_chars:>9,}")

    # Before/after comparison for one PDF page.
    index = next(i for i, d in enumerate(loaded)
                 if d.metadata["file_name"] == "leave-and-attendance-policy.pdf"
                 and d.metadata["page_number"] == 6)
    print("\nBEFORE (leave-and-attendance-policy.pdf, page 6):")
    print("-" * 60)
    print(loaded[index].page_content[:300])
    print("-" * 60)
    print("AFTER:")
    print("-" * 60)
    print(cleaned[index].page_content[:300])
    print("-" * 60)
    print("Metadata kept:", cleaned[index].metadata["source"], "page", cleaned[index].metadata["page_number"])
    print(f"\nSaved to: {OUTPUT_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
