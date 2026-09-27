# HR RAG Assistant — Start Here

## What we are building

A simple internal HR assistant.

An employee asks a question such as:

- How many casual leaves do I get?
- What is my notice period?
- What should I do on my first day?

The system finds the relevant HR policy text and gives a short answer with the source document and page number.


## Technology we will use

- Python
- LangChain document loaders
- LangChain RecursiveCharacterTextSplitter
- Sentence Transformers
- Embedding model: `sentence-transformers/all-MiniLM-L12-v2`
- Vector database: Chroma
- Reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- LLM: DeepSeek `deepseek-v4-flash`
- Frontend: Streamlit

## Raw documents

Put all sample HR documents inside:

```text
data/raw/
```



## The build order

Build one phase at a time. Do not ask Claude code to build the entire application in one shot.

```text
PHASE 00  Project setup
PHASE 01  Load documents
PHASE 02  Clean / normalize
PHASE 03  Chunk documents
PHASE 04  Create embeddings
PHASE 05  Store in Chroma
PHASE 06  Embed question + retrieve chunks
PHASE 07  Rerank retrieved chunks
PHASE 08  Build prompt + call DeepSeek + citations
PHASE 09  Build Streamlit interface
PHASE 10  Connect everything end to end
```

## Why we build it this way


```text
Raw file
  ↓
loaded_documents.jsonl
  ↓
cleaned_documents.jsonl
  ↓
chunks.jsonl
  ↓
embedding_preview.json
  ↓
Chroma database
  ↓
retrieval_preview.json
  ↓
reranked_preview.json
  ↓
prompt_preview.txt + answer
  ↓
Streamlit HR Assistant
```

This makes the RAG pipeline visible instead of hiding everything behind one framework call.

## How to use the phase files

1. Place the raw HR documents in `data/raw/`.
2. Open the project in Codex.
3. Give Codex `claude.md` as the project rules.
4. Start with `phases/PHASE_00_PROJECT_SETUP.md`.
5. Let Codex complete only that phase.
6. Run it and inspect the output.
7. Then move to the next phase.

Do not skip ahead if the current phase does not work.
