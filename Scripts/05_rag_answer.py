"""
Week 3: Retrieval-augmented compliance risk answer.

This script:
1. Accepts a user question.
2. Retrieves relevant chunks using the retrieval logic from 04_retrieve_chunks.py.
3. Sends only the retrieved chunks to Claude.
4. Requires a grounded answer with source references, unknowns, confidence, and human-review guidance.

This is the first end-to-end RAG answer loop.
"""

import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from importlib.machinery import SourceFileLoader


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

RETRIEVAL_SCRIPT = PROJECT_ROOT / "Scripts" / "04_retrieve_chunks.py"
CHUNKS_FILE = PROJECT_ROOT / "Data" / "processed_chunks.json"

DEFAULT_QUESTION = "Who owns Northbridge Industrial Components Ltd.?"

MODEL_NAME = "claude-sonnet-4-5"
MAX_TOKENS = 1000

NO_RELEVANT_EVIDENCE_MESSAGE = """
Answer:
Insufficient evidence. No relevant evidence was retrieved above the similarity threshold.

Evidence used:
None. The retrieval layer did not return any chunks that met the minimum similarity threshold.

Source references:
None.

Unknowns or conflicting information:
The available source corpus does not contain retrieved evidence that supports answering this question.

Confidence:
Low for answering the question; high that the current retrieved evidence is insufficient.

Human review required:
Yes. A human analyst should gather additional relevant sources before making a compliance or risk judgment.
""".strip()


retrieval_module = SourceFileLoader(
    "retrieve_chunks_module",
    str(RETRIEVAL_SCRIPT),
).load_module()


def format_retrieved_evidence(retrieved_chunks: list[dict]) -> str:
    """
    Format retrieved chunks as evidence for Claude.
    """
    evidence_blocks = []

    for rank, chunk in enumerate(retrieved_chunks, start=1):
        evidence_block = f"""
RETRIEVED_CHUNK_{rank}
Chunk ID: {chunk["chunk_id"]}
Source ID: {chunk["source_id"]}
Source name: {chunk["source_name"]}
Source date: {chunk["source_date"]}
Source type: {chunk["source_type"]}
Entity: {chunk["entity"]}
Similarity score: {chunk["similarity_score"]:.4f}

Text:
{chunk["text"]}
""".strip()

        evidence_blocks.append(evidence_block)

    return "\n\n---\n\n".join(evidence_blocks)


def build_prompt(question: str, evidence: str) -> str:
    """
    Build a grounded answer prompt using retrieved evidence only.
    """
    return f"""
You are helping a compliance and third-party risk analyst review a vendor.

Answer the user question using only the RETRIEVED EVIDENCE below.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- Do not treat retrieved evidence as automatically true.
- Distinguish confirmed facts from possible risks.
- If the retrieved evidence does not support an answer, state "Insufficient evidence."
- If sources conflict, explain the conflict rather than deciding which source is correct.
- Reference source names and chunk IDs exactly.
- Recommend human review when material questions remain unresolved.
- Similarity scores are retrieval ranking signals, not factual confidence.

Return the answer using this exact structure:

Answer:
Evidence used:
Source references:
Unknowns or conflicting information:
Confidence:
Human review required:

USER QUESTION:
{question}

RETRIEVED EVIDENCE:
{evidence}
""".strip()


def get_rag_answer(question: str) -> tuple[list[dict], str]:
    """
    Retrieve evidence and ask Claude for a grounded answer.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found. Add it to your .env file.")

    chunks = retrieval_module.load_chunks(CHUNKS_FILE)
    retrieved_chunks = retrieval_module.retrieve_chunks(question, chunks)

    if not retrieved_chunks:
        return retrieved_chunks, NO_RELEVANT_EVIDENCE_MESSAGE

    evidence = format_retrieved_evidence(retrieved_chunks)
    prompt = build_prompt(question, evidence)

    client = Anthropic(api_key=api_key)

    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    return retrieved_chunks, message.content[0].text


def print_retrieved_chunks(question: str, retrieved_chunks: list[dict]) -> None:
    """
    Print retrieved chunks before the Claude answer.
    """
    print("\nQuestion:")
    print(question)

    if not retrieved_chunks:
        print("\nNo relevant evidence retrieved above the similarity threshold.")
        print("Claude was not called because the retrieval layer did not return usable evidence.\n")
        return

    print("\nRetrieved evidence sent to Claude:\n")

    for rank, chunk in enumerate(retrieved_chunks, start=1):
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Similarity score: {chunk['similarity_score']:.4f}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source name: {chunk['source_name']}")
        print(f"Source date: {chunk['source_date']}")
        print(f"Source type: {chunk['source_type']}")
        print("\nText:")
        print(chunk["text"])
        print()


def main():
    """
    Run the RAG answer flow for a question.

    Usage:
    python3 Scripts/05_rag_answer.py
    python3 Scripts/05_rag_answer.py "Is Daniel Vermeer confirmed to be sanctioned?"
    """
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = DEFAULT_QUESTION

    try:
        retrieved_chunks, answer = get_rag_answer(question)

        print_retrieved_chunks(question, retrieved_chunks)

        print("\nClaude grounded answer:\n")
        print(answer)

    except Exception as error:
        print("Error running RAG answer script:")
        print(error)


if __name__ == "__main__":
    main()