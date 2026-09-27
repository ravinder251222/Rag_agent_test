# Phase 08 — Build the Prompt, Call DeepSeek, Return Citations

## Goal

Complete the RAG answer-generation stage.

This phase covers:

```text
Instructions
+
Best retrieved chunks
+
User question
   ↓
DeepSeek
   ↓
Grounded answer + citations
```

## LLM

Use the current DeepSeek API model:

```text
deepseek-v4-flash
```

Read the API key from:

```text
DEEPSEEK_API_KEY
```

Never hard-code the key.

## What Codex should build

Create:

```text
src/rag.py
```

Reuse the existing functions from retrieval and reranking rather than rewriting those stages.

## Prompt rules

Build a simple explicit prompt with three visible parts:

```text
SYSTEM INSTRUCTIONS
RETRIEVED CONTEXT
USER QUESTION
```

The system instructions should tell DeepSeek:

- answer only from the supplied HR context,
- do not invent company policy,
- if the answer is not supported, say it cannot be found in the provided HR documents,
- keep the answer direct,
- do not invent citations.

## Citation design

Do not depend on the LLM to invent source names.

Assign each supplied context chunk a context label such as:

```text
[S1]
[S2]
[S3]
[S4]
```

Each label should be tied in Python to trusted metadata:

```text
S1 → leave_policy.pdf, page 3
S2 → employee_handbook.pdf, page 12
```

Ask the model to cite only these labels in the answer.

After generation, return the answer plus a clean source list generated from the metadata.

## artifacts

Save:

```text
artifacts/prompt_preview.txt
artifacts/answer_preview.json
```

`prompt_preview.txt` should show the exact prompt sent to DeepSeek with no secret values.

`answer_preview.json` should contain:

- question,
- final answer,
- cited source labels,
- source file names,
- page numbers when available.



## Test missing information

Also test a question whose answer is NOT present in the HR documents.

The assistant should refuse to guess and say that the answer cannot be found in the provided HR documents.

## Proof that this phase works

A known HR question returns a grounded answer and source/page information, while an unsupported question does not produce invented policy.

## Stop condition

Stop after terminal-based RAG answers with citations work reliably.
