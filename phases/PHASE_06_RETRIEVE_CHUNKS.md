# Phase 06 — Embed a Question and Retrieve Relevant Chunks

## Goal

Build the first query-time part of the RAG pipeline.

This phase covers:

```text
User question
   ↓
Same embedding model
   ↓
Query vector
   ↓
Chroma similarity search
   ↓
Candidate chunks
```

## What Codex should build

Create:

```text
src/retrieve.py
```

## Behavior

The script should accept a plain-English HR question from the terminal.

Example:

```text
How many casual leaves do I get?
```

Then:

1. Use the same embedding model used for the stored document chunks.
2. Search the existing Chroma collection.
3. Retrieve a small candidate set, starting with `top_k = 8`.
4. Return both the chunk text and metadata.
5. Return the similarity/distance information that Chroma provides, if available through the chosen API.


Save the latest query and candidates to:

```text
artifacts/retrieval_preview.json
```

Include:

- original question,
- retrieved rank,
- chunk ID,
- source,
- page,
- retrieval score or distance,
- chunk text.

## What to print

Print the candidates in ranked order.



At this phase there should be NO LLM call.

The system is only finding likely relevant chunks.

## Proof that this phase works

Ask several questions whose answers are known to exist in the HR sample documents. Relevant policy passages should appear near the top.


