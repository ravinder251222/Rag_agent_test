"""Phase 00: print a simple inventory of the raw HR files.

This only lists file names and extensions. It does not read file contents.
"""

from collections import Counter
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# System files that are not HR documents.
IGNORED_NAMES = {".DS_Store"}


def list_raw_files(raw_dir: Path = RAW_DIR) -> list[Path]:
    """Return every raw file under data/raw/, sorted, skipping system files."""
    files = []
    for path in sorted(raw_dir.rglob("*")):
        if path.is_file() and path.name not in IGNORED_NAMES:
            files.append(path)
    return files


def main() -> None:
    files = list_raw_files()

    print(f"Raw folder: {RAW_DIR}")
    print(f"Total files: {len(files)}\n")

    print(f"{'Folder':<12} {'File name':<42} {'Ext':<6} {'Size (KB)':>9}")
    print("-" * 72)
    for path in files:
        folder = path.parent.relative_to(RAW_DIR).as_posix()
        size_kb = path.stat().st_size / 1024
        print(f"{folder:<12} {path.name:<42} {path.suffix:<6} {size_kb:>9.1f}")

    print("\nFiles by extension:")
    counts = Counter(path.suffix.lower() for path in files)
    for ext, count in sorted(counts.items()):
        print(f"  {ext:<6} {count}")


if __name__ == "__main__":
    main()
