"""
Semantic retrieval for the Compliance Risk RAG Assistant.

This script retrieves source chunks by meaning similarity instead of keyword overlap.
It uses sentence-transformers/all-MiniLM-L6-v2 to embed both the user question and
the source chunks, then ranks chunks by cosine similarity.

This is intentionally kept separate from Scripts/04_retrieve_chunks.py so the
project can compare sparse keyword retrieval against semantic embedding retrieval.
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_FILE = PROJECT_ROOT / "Data" / "processed_chunks.json"

MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3
MIN_SIMILARITY_SCORE = 0.20


def load_chunks(chunks_file: Path = CHUNKS_FILE) -> list[dict]:
    """
    Load processed source chunks from JSON.
    """
    if not chunks_file.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {chunks_file}. "
            "Run Scripts/03_build_chunks.py first."
        )

    with chunks_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two embedding vectors.

    Cosine similarity measures whether two vectors point in a similar direction.
    Higher scores mean the texts are closer in meaning.
    """
    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)

    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)


def embed_chunks(model: SentenceTransformer, chunks: list[dict]) -> list[dict]:
    """
    Create embeddings for every chunk while preserving metadata.
    """
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(chunk_texts)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding,
            }
        )

    return embedded_chunks


def retrieve_chunks(
    question: str,
    embedded_chunks: list[dict],
    model: SentenceTransformer,
    top_k: int = TOP_K,
    min_similarity_score: float = MIN_SIMILARITY_SCORE,
) -> list[dict]:
    """
    Retrieve chunks by semantic similarity to the user question.
    """
    question_embedding = model.encode(question)
    scored_chunks = []

    for chunk in embedded_chunks:
        score = cosine_similarity(question_embedding, chunk["embedding"])

        scored_chunk = {
            **chunk,
            "similarity_score": score,
        }

        scored_chunks.append(scored_chunk)

    ranked_chunks = sorted(
        scored_chunks,
        key=lambda item: item["similarity_score"],
        reverse=True,
    )

    relevant_chunks = [
        chunk
        for chunk in ranked_chunks
        if chunk["similarity_score"] >= min_similarity_score
    ]

    return relevant_chunks[:top_k]


def print_results(question: str, results: list[dict]) -> None:
    """
    Print semantic retrieval results in a reviewable format.
    """
    print("\nQuestion:")
    print(question)

    if not results:
        print("\nNo relevant semantic evidence retrieved above the similarity threshold.")
        print(f"Minimum semantic similarity threshold: {MIN_SIMILARITY_SCORE:.4f}")
        return

    print(f"\nTop {len(results)} semantic retrieved chunks above threshold:\n")

    for rank, chunk in enumerate(results, start=1):
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source_name']}")
        print(f"Source date: {chunk['source_date']}")
        print(f"Source type: {chunk['source_type']}")
        print(f"Similarity score: {chunk['similarity_score']:.4f}")
        print("\nPreview:")
        print(chunk["text"][:500])
        print()


def main() -> None:
    """
    Run semantic retrieval from the command line.
    """
    import sys

    if len(sys.argv) < 2:
        raise ValueError(
            'Please provide a question. Example: '
            'python3 Scripts/06_semantic_retrieve_chunks.py "Who owns Northbridge?"'
        )

    question = " ".join(sys.argv[1:])

    chunks = load_chunks()
    model = SentenceTransformer(MODEL_NAME)
    embedded_chunks = embed_chunks(model, chunks)
    results = retrieve_chunks(question, embedded_chunks, model)

    print_results(question, results)


if __name__ == "__main__":
    main()