# Project Map

This is the target shape of the project after all phases are complete.

```text
hr-rag-assistant/
│
├── AGENTS.md
├── START_HERE.md
├── .env
├── .env.example
├── requirements.txt
├── app.py
│
├── data/
│   ├── raw/
│   │   └── original HR documents
│   ├── processed/
│   │   ├── loaded_documents.jsonl
│   │   ├── cleaned_documents.jsonl
│   │   └── chunks.jsonl
│   └── chroma/
│       └── persisted Chroma database
│
├── artifacts/
│   ├── embedding_preview.json
│   ├── retrieval_preview.json
│   ├── reranked_preview.json
│   ├── prompt_preview.txt
│   └── answer_preview.json
│
└── src/
    ├── load_documents.py
    ├── clean_documents.py
    ├── chunk_documents.py
    ├── embeddings.py
    ├── build_index.py
    ├── retrieve.py
    ├── rerank.py
    └── rag.py
```

Do not create all of these files in Phase 00. This map only shows where the project is heading.

## Final data flow

```text
data/raw
   ↓
load_documents.py
   ↓
loaded_documents.jsonl
   ↓
clean_documents.py
   ↓
cleaned_documents.jsonl
   ↓
chunk_documents.py
   ↓
chunks.jsonl
   ↓
embeddings.py
   ↓
embedding vectors
   ↓
build_index.py
   ↓
Chroma

User question
   ↓
retrieve.py
   ↓
candidate chunks
   ↓
rerank.py
   ↓
best chunks
   ↓
rag.py
   ↓
DeepSeek
   ↓
answer + citations
   ↓
app.py
```
