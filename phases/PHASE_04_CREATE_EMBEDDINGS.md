# Phase 04 — Convert Chunks into Embeddings

## Goal

Each text chunk becomes its own numerical vector.

This phase covers:

```text
Chunk
  ↓
Embedding model
  ↓
Vector
```

## Embedding model

Use:

```text
sentence-transformers/all-MiniLM-L12-v2
```

Use the Sentence Transformers library directly or through a very thin LangChain embedding wrapper. Keep the logic easy to see.

## What Codex should build

Create:

```text
src/embeddings.py
```

The script should:

1. Read `data/processed/chunks.jsonl`.
2. Load the embedding model once.
3. Embed the chunks.
4. Make it clear in the code that one chunk produces one vector.
5. Print the vector dimension.
6. Demonstrate that multiple chunks may be embedded as a batch while still producing one vector per chunk.



For the first few chunks store only:

- `chunk_id`
- a short text preview
- vector dimension
- first 10 vector numbers

Example mental model:

```text
Chunk 1 → 384-number vector
Chunk 2 → 384-number vector
Chunk 3 → 384-number vector
```



## Do not do yet

Do not create the Chroma database in this phase.


## Proof that this phase works

- embedding model loads,
- every tested chunk gets one vector,
- the vectors have the expected fixed dimension,
- `embedding_preview.json` exists.

## Stop condition

Stop after the embedding transformation is visible and understandable.
