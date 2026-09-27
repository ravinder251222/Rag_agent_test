# Phase 01 — Load the Raw Documents

## Goal

Read the raw HR files and convert them into LangChain `Document` objects.

This phase covers:

```text
Raw files
   ↓
Document loaders
   ↓
Document objects
```

## What Codex should build

Create:

```text
src/load_documents.py
```

The script should:

1. Read files from `data/raw/`.
2. Select an appropriate LangChain loader for each file type that actually exists.
3. Load the content into separate LangChain `Document` objects.
4. Preserve useful metadata from the loader.
5. Add simple normalized metadata such as:
   - `source`
   - `file_name`
   - `file_type`
6. For PDFs, preserve page metadata and create a human-friendly 1-based page number for citations if needed.
7. Save a human-readable copy to:

```text
data/processed/loaded_documents.jsonl
```

Each JSONL row should represent ONE Document object.

## Important rule

Do not combine all files into one giant document.

A 20-page PDF may create many Document objects, for example one per page. That is correct.

## What to print

After running, print:

- number of raw files,
- number of Document objects created,
- count by source file,
- a short preview of one Document's text,
- its metadata.



## Do not do yet

Do not clean, chunk, embed or store anything in Chroma.

## Proof that this phase works

We will be able to see extracted text and its original source metadata in `loaded_documents.jsonl`.

## Stop condition

Stop when all supported raw documents load successfully and the JSONL file has been created.
