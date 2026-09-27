# Phase 03 — Split Documents into Chunks

## Goal

Turn long cleaned Document objects into smaller searchable passages.


## What Codex should build

Create:

```text
src/chunk_documents.py
```

Read:

```text
data/processed/cleaned_documents.jsonl
```

Use LangChain `RecursiveCharacterTextSplitter`.

Start with:

```text
chunk_size = 800 characters
chunk_overlap = 120 characters
```

Keep these values in clear constants near the top of the file
## Metadata

Every chunk must keep the source metadata of its parent Document.

Also add:

- `chunk_id`
- `chunk_index`

Use a readable `chunk_id`, for example a combination of file name, page and chunk number.

## Save the chunks

Write:

```text
data/processed/chunks.jsonl
```

One JSONL row = one chunk.

Do not merge chunks back together.

## What to print

Print:

- number of cleaned Document objects,
- number of chunks created,
- first 2 or 3 chunks,
- metadata for each preview chunk,
- character length of each preview chunk.
.


## Do not do yet

Do not create embeddings or Chroma.
