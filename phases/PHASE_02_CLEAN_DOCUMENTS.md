# Phase 02 — Clean and Normalize the Text

## Goal

Clean the loaded text without changing its meaning.



## What Claud should build

Create:

```text
src/clean_documents.py
```

It should read:

```text
data/processed/loaded_documents.jsonl
```

and write:

```text
data/processed/cleaned_documents.jsonl
```

## Keep cleaning conservative

Use only simple cleaning that is safe for HR documents, such as:

- normalize repeated spaces,
- normalize excessive blank lines,
- repair obvious broken whitespace,
- remove clearly repeated boilerplate only if it can be detected safely,
- remove obvious standalone page-number text only when page metadata is preserved separately.

Do not aggressively rewrite sentences.

Do not summarize the content.

Do not use the LLM for cleaning.

## Preserve metadata

The cleaned Document must keep the original metadata.

Cleaning should change `page_content`, not destroy source information.


## Proof that this phase works

`cleaned_documents.jsonl` exists, contains the same source relationships, and the text is cleaner without losing useful policy information.

## Stop condition

Stop after the before/after cleaning comparison is easy to show.
