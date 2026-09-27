# Phase 00 — Project Setup

## Goal

Create the simplest project structure required for the RAG application.

Do not build the RAG logic yet.

## What Codex should do

1. Inspect the files already present inside `data/raw/`.
2. Print a simple inventory of the file names and extensions.
3. Create only the base folders and setup files needed for the next phases.
4. Create a Python virtual environment only if one does not already exist.
5. Create `requirements.txt` with the packages needed for this project.
6. Create `.env.example` containing `DEEPSEEK_API_KEY=`.
7. Make sure `.env` is ignored by Git.

## Keep dependencies simple

We expect packages for:

- LangChain loaders and text splitting
- PDF parsing if PDFs are present
- Chroma
- Sentence Transformers
- DeepSeek through an OpenAI-compatible client
- Streamlit
- dotenv

Only add loader dependencies for source formats that actually exist in `data/raw/`.

## Do not do yet

Do not:

- load document contents,
- clean text,
- chunk text,
- create embeddings,
- create Chroma,
- call DeepSeek,
- build Streamlit.



## Stop condition

Stop after setup and file inventory work correctly.
