"""Phase 08: build the prompt, call DeepSeek, return a cited answer.

    question -> retrieve (Phase 06) -> rerank (Phase 07)
             -> label best chunks [S1]..[S4] -> prompt -> DeepSeek
             -> answer + sources built from trusted metadata

Citations never come from the LLM's imagination: each label [S1], [S2] ...
is tied in Python to the chunk's file name and page. The model may only cite
those labels, and the source list is rebuilt from our own metadata.

Usage:
    python src/rag.py "How many casual leaves do I get?"

Output: artifacts/prompt_preview.txt, artifacts/answer_preview.json
"""

import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from rerank import rerank, save_rerank_preview
from retrieve import retrieve, save_retrieval_preview

DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
NOT_FOUND_MESSAGE = "I cannot find the answer to this in the provided HR documents."

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROMPT_PREVIEW_FILE = PROJECT_DIR / "artifacts" / "prompt_preview.txt"
ANSWER_PREVIEW_FILE = PROJECT_DIR / "artifacts" / "answer_preview.json"

SYSTEM_INSTRUCTIONS = f"""You are an internal HR assistant for Nexora Technologies.

Rules:
1. Answer ONLY from the HR context provided below. Do not use outside knowledge.
2. Do not invent or assume company policy.
3. If the context does not contain the answer, reply exactly:
   "{NOT_FOUND_MESSAGE}"
4. Keep the answer short and direct.
5. After each fact, cite the context label it came from, e.g. [S1] or [S2][S3].
   Only use the labels given in the context. Never invent sources or labels.
6. If sources disagree, say so briefly and cite each side. Only say which one
   applies if the context itself states which document, version or date prevails."""


def label_sources(chunks: list[dict]) -> list[dict]:
    """Give each context chunk a label S1, S2, ... tied to its trusted metadata."""
    sources = []
    for number, chunk in enumerate(chunks, start=1):
        sources.append({
            "label": f"S{number}",
            "file_name": chunk["file_name"],
            "source": chunk["source"],
            "page": chunk["page"],
            "location": chunk["location"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
        })
    return sources


def build_context(sources: list[dict]) -> str:
    blocks = []
    for s in sources:
        header = f"[{s['label']}] {s['file_name']}" + (f", {s['location']}" if s["location"] else "")
        blocks.append(f"{header}\n{s['text']}")
    return "\n\n".join(blocks)


def build_prompt(question: str, sources: list[dict]) -> tuple[str, str]:
    """Return (system message, user message). Three visible parts in total."""
    user_message = (
        "RETRIEVED CONTEXT\n"
        "=================\n"
        f"{build_context(sources)}\n\n"
        "USER QUESTION\n"
        "=============\n"
        f"{question}"
    )
    return SYSTEM_INSTRUCTIONS, user_message


def call_deepseek(system_message: str, user_message: str) -> str:
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is missing. Add it to the .env file.")

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


def cited_labels(answer: str, sources: list[dict]) -> list[str]:
    """Return the valid labels the answer actually cites, in label order."""
    found = set(re.findall(r"\[(S\d+)\]", answer))
    return [s["label"] for s in sources if s["label"] in found]


def save_prompt_preview(system_message: str, user_message: str) -> None:
    PROMPT_PREVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"MODEL: {DEEPSEEK_MODEL}\n\n"
        "SYSTEM INSTRUCTIONS\n"
        "===================\n"
        f"{system_message}\n\n"
        f"{user_message}\n"
    )
    PROMPT_PREVIEW_FILE.write_text(text, encoding="utf-8")


def save_answer_preview(result: dict) -> None:
    output = {
        "question": result["question"],
        "answer": result["answer"],
        "cited_labels": result["cited_labels"],
        "citations": [
            {k: s[k] for k in ("label", "file_name", "source", "page", "location")}
            for s in result["citations"]
        ],
    }
    ANSWER_PREVIEW_FILE.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")


def answer_question(question: str) -> dict:
    """Run the full question-time pipeline and return every stage's output."""
    candidates = retrieve(question)
    best_chunks = rerank(question, candidates)
    sources = label_sources(best_chunks)
    system_message, user_message = build_prompt(question, sources)

    answer = call_deepseek(system_message, user_message)
    labels = cited_labels(answer, sources)
    if answer.startswith(NOT_FOUND_MESSAGE):
        # A "not found" answer has no supporting source, so list none.
        labels = []

    return {
        "question": question,
        "answer": answer,
        "cited_labels": labels,
        "citations": [s for s in sources if s["label"] in labels],
        "candidates": candidates,
        "reranked": best_chunks,
        "sources": sources,
        "system_message": system_message,
        "user_message": user_message,
    }


def save_all_previews(result: dict) -> None:
    save_retrieval_preview(result["question"], result["candidates"])
    save_rerank_preview(result["question"], result["candidates"], result["reranked"])
    save_prompt_preview(result["system_message"], result["user_message"])
    save_answer_preview(result)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    question = " ".join(sys.argv[1:]) or input("Ask an HR question: ")
    result = answer_question(question)
    save_all_previews(result)

    print(f"Question: {question}\n")
    print("Answer:")
    print(result["answer"])
    print("\nSources:")
    if not result["citations"]:
        print("  (none cited)")
    for s in result["citations"]:
        where = f", {s['location']}" if s["location"] else ""
        print(f"  [{s['label']}] {s['file_name']}{where}")

    print(f"\nSaved to: {PROMPT_PREVIEW_FILE.relative_to(PROJECT_DIR)}, "
          f"{ANSWER_PREVIEW_FILE.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
