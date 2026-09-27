# Phase 10 — End-to-End Check

## Goal

Verify the complete RAG pipeline and make it ready for use.

Do not add advanced features.

## Final pipeline that must be visible

```text
RAW HR DOCUMENTS
      ↓
LOADERS
      ↓
DOCUMENT OBJECTS
      ↓
CLEANING
      ↓
CHUNKS + METADATA
      ↓
EMBEDDINGS
      ↓
CHROMA
      ↓
USER QUESTION
      ↓
QUERY EMBEDDING
      ↓
RETRIEVAL
      ↓
RERANKING
      ↓
PROMPT
      ↓
DEEPSEEK
      ↓
ANSWER + CITATIONS
```

## What Codex should do

1. Run every offline/indexing stage from a clean state.
2. Confirm the Chroma index is created without duplicate records.
3. Start the Streamlit app.
4. Test at least five questions that are answered by different source documents.
5. Test at least two questions that are not answered in the documents.
6. Confirm citations point back to the correct source and page when page information exists.
7. Confirm no LLM is used during loading, cleaning, chunking, embedding, storage, retrieval or reranking.
8. Confirm the same embedding model is used for chunks and queries.
9. Confirm the app does not answer unsupported HR questions as if they were company policy.
10. Keep all intermediate artifacts available.

## Inspection order

For one example question, show these files/screens in order:

```text
1. Original file in data/raw/
2. loaded_documents.jsonl
3. cleaned_documents.jsonl
4. chunks.jsonl
5. embedding_preview.json
6. Chroma record count
7. retrieval_preview.json
8. reranked_preview.json
9. prompt_preview.txt
10. answer_preview.json
11. Streamlit final answer
```

## Final verification questions

Verify the following:

1. What did the loader create?
2. Why did we clean before chunking?
3. Why did we split the document?
4. Does one chunk get one vector or many final vectors?
5. What does Chroma store and search?
6. Why must the question use the same embedding space?
7. What is the difference between retrieval and reranking?
8. What exactly is placed into the LLM prompt?
9. Where do citations come from?
10. Which parts happen once during indexing and which happen for every question?

If these questions can be answered, the core RAG pipeline is working as intended.

## Do not add

Do not add advanced production RAG techniques yet.

Those can be added separately after the core pipeline is stable.
