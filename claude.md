# Codex Project Instructions

Build this rag project phase by phase
## Main rule

Keep the code simple, explicit and easy to read.

Do not hide the complete RAG pipeline inside one large LangChain chain.


## Project

We are building an internal HR RAG assistant using documents stored in `data/raw/`.

## Fixed stack

- Python
- LangChain document loaders
- `RecursiveCharacterTextSplitter`
- `sentence-transformers/all-MiniLM-L12-v2` for embeddings
- Chroma as the vector database
- `cross-encoder/ms-marco-MiniLM-L-6-v2` for reranking
- DeepSeek model `deepseek-v4-flash`
- Streamlit frontend

## Important implementation rules

1. Build only the phase requested by the current phase file.
2. Do not build future phases early.
3. Use small Python modules with clear names.
4. Prefer normal Python functions over complex abstractions.
6. Preserve metadata from the original source.
7. For PDFs, preserve page information so answers can cite the page.
8. Never merge all documents into one giant text string.
9. Keep documents and chunks as separate records.
10. Every chunk must get its own embedding.
11. Use the same embedding model for document chunks and user questions.
12. Make cleaning conservative. Do not delete useful HR policy content.
13. Do not make reranking part of initial vector search. Keep it as a separate visible step.
14. The LLM must answer only from retrieved context.
15. If the context does not support an answer, the assistant must clearly say it cannot find the answer in the provided HR documents.
16. Return citations using preserved metadata.
17. Do not add authentication, Docker, cloud deployment, queues, agents, background jobs, or production infrastructure unless explicitly requested later.
18. Do not add hybrid search, parent-child retrieval, query rewriting, evaluation frameworks, or other advanced RAG features in the initial build.


Use these folders:

```text
data/raw/
data/processed/
data/chroma/
artifacts/
src/
```

Keep output files human-readable whenever possible.

## Environment variables

Use `.env` for secrets.

Expected key:

```text
DEEPSEEK_API_KEY=
```

Never hard-code API keys.

## Before finishing a phase

- Run the code for that phase.
- Fix errors.
- Print a small readable summary of what was created.
- Stop. Do not automatically continue to the next phase.
