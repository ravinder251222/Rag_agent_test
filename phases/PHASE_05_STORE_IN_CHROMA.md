# Phase 05 — Store Chunks in Chroma

## Goal

Create the searchable vector knowledge base.

This phase covers:

```text
Chunk text
+
Embedding vector
+
Metadata
   ↓
Chroma vector database
```

## What Codex should build

Create:

```text
src/build_index.py
```

Use the SAME embedding model from Phase 04.

Read the chunk records from:

```text
data/processed/chunks.jsonl
```

Store them in a persistent Chroma collection inside:

```text
data/chroma/
```

## Every stored record should keep

- chunk text,
- chunk embedding,
- chunk ID,
- source file,
- page number when available,
- other useful metadata already preserved.

## Important behavior

Make rebuilding the index predictable.

When running the indexing script, it should either:

- safely recreate the collection, or
- clearly explain that it is reusing an existing collection.

Avoid silently duplicating every chunk each time the script runs.

## What to print

Print:

- collection name,
- number of chunks inserted,
- final number of records,
- one stored record's metadata,
- Chroma persistence directory.



## Proof that this phase works

The `data/chroma/` directory exists and the record count matches the chunks we expected to index.

## Stop condition

Stop after the knowledge base is persisted and its record count can be shown.
