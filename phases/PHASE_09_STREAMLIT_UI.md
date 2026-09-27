# Phase 09 — Build the Streamlit Interface

## Goal

Put the working RAG pipeline behind a simple user-friendly interface.

Do not change the RAG logic in this phase.

## What Codex should build

Create:

```text
app.py
```

Use Streamlit.

## Main UI

Keep the default screen simple:

```text
HR Policy Assistant

[ Ask an HR question...                 ]
[ Ask ]

Answer
...

Sources
- leave_policy.pdf — page 3
- employee_handbook.pdf — page 12
```

## Citation/source behavior

For each source, show:

- file name,
- page number when available,
- short supporting text excerpt.

If Streamlit can safely expose the local sample source file from this project, provide an open/download control for that document. Do not fake web URLs for local files.

## Add one expander

Add an expandable area called something like:

```text
See how this RAG answer was created
```

Inside it show the pipeline stages for the current question:

1. user question,
2. retrieved candidates,
3. reranked chunks,
4. final context sent to DeepSeek.

Keep this hidden by default so the normal HR assistant remains clean.

## Important rule

The Streamlit app must call functions from `src/`.

Do not copy the whole pipeline into `app.py`.


## Proof that this phase works

Run:

```text
streamlit run app.py
```


## Stop condition

Stop after the interface works with the already-built pipeline.
