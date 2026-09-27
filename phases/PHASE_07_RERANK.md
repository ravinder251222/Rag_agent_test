# Phase 07 — Rerank the Retrieved Chunks

## Goal

Show the difference between fast retrieval and more careful relevance scoring.

This phase covers:

```text
8 retrieved candidates
      ↓
Reranker
      ↓
Best 3 or 4 chunks
```

## Reranker

Use a small local cross-encoder:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Keep reranking separate from Chroma retrieval so both stages remain visible.

## What Codex should build

Create:

```text
src/rerank.py
```

The function should receive:

- user question,
- retrieved candidate chunks.

For every candidate, score the pair:

```text
(question, chunk text)
```

Then sort candidates from most relevant to least relevant.

Keep the best `top_n = 4` for the next phase.

## Output artifact

Save:

```text
artifacts/reranked_preview.json
```

Include both:

- original retrieval rank,
- new reranker rank,
- reranker score,
- source metadata,
- chunk text.




Explain:

> Retrieval quickly creates a shortlist. Reranking looks at the question and each shortlisted chunk more carefully and chooses the strongest context.

## Do not do yet

Do not call DeepSeek.

## Proof that this phase works

The script can show the original order and reranked order for the same question.

## Stop condition

Stop once reranking is a clearly visible independent stage.
