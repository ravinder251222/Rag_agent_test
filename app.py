"""Phase 09: Streamlit interface for the HR RAG assistant.

All RAG logic lives in src/. This file only shows inputs and results.

Run:
    streamlit run app.py
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR / "src"))

from rag import answer_question, save_all_previews  # noqa: E402

EXCERPT_LENGTH = 300


def source_title(source: dict) -> str:
    where = f" — {source['location']}" if source["location"] else ""
    return f"[{source['label']}] {source['file_name']}{where}"


def show_download(source: dict, key: str) -> None:
    """Offer the local source file for download. No fake web URLs."""
    path = PROJECT_DIR / source["source"]
    if path.is_file():
        st.download_button(
            label=f"Download {source['file_name']}",
            data=path.read_bytes(),
            file_name=source["file_name"],
            key=key,
        )


def show_sources(citations: list[dict]) -> None:
    st.subheader("Sources")
    if not citations:
        st.caption("No sources cited.")
        return
    for source in citations:
        st.markdown(f"**{source_title(source)}**")
        excerpt = source["text"][:EXCERPT_LENGTH].strip()
        st.caption(excerpt + ("..." if len(source["text"]) > EXCERPT_LENGTH else ""))
        show_download(source, key=f"download-{source['label']}")


def show_pipeline(result: dict) -> None:
    with st.expander("See how this RAG answer was created", expanded=False):
        st.markdown("**1. User question**")
        st.write(result["question"])

        st.markdown(f"**2. Retrieved candidates** (Chroma, top {len(result['candidates'])})")
        st.dataframe(
            [{"rank": c["retrieval_rank"], "similarity": c["similarity"],
              "chunk_id": c["chunk_id"], "text": c["text"][:120]} for c in result["candidates"]],
            hide_index=True,
        )

        st.markdown(f"**3. Reranked chunks** (cross-encoder, best {len(result['reranked'])})")
        st.dataframe(
            [{"new rank": c["rerank_rank"], "was rank": c["retrieval_rank"],
              "rerank score": c["rerank_score"], "chunk_id": c["chunk_id"]} for c in result["reranked"]],
            hide_index=True,
        )

        st.markdown("**4. Final context sent to DeepSeek**")
        st.code(result["system_message"] + "\n\n" + result["user_message"], language=None)


def main() -> None:
    st.set_page_config(page_title="HR Policy Assistant")
    st.title("HR Policy Assistant")
    st.caption("Answers come only from Nexora's HR documents, with sources.")

    with st.form("question_form"):
        question = st.text_input("Ask an HR question...", placeholder="How many casual leaves do I get?")
        asked = st.form_submit_button("Ask")

    if asked and question.strip():
        with st.spinner("Searching the HR documents..."):
            try:
                result = answer_question(question.strip())
                save_all_previews(result)
                st.session_state["result"] = result
            except Exception as error:
                st.error(f"Something went wrong: {error}")
                return

    result = st.session_state.get("result")
    if result:
        st.subheader("Answer")
        st.markdown(result["answer"])
        show_sources(result["citations"])
        show_pipeline(result)


main()
