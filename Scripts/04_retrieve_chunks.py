"""
Week 3: Retrieve relevant source chunks.

This script:
1. Loads processed source chunks from Data/processed_chunks.json.
2. Accepts a user question.
3. Expands certain domain-specific query terms.
4. Scores each chunk against the question using lightweight text similarity.
5. Ranks the chunks.
6. Prints the top retrieved chunks with metadata.

This is still a lightweight retrieval baseline.
It does not call Claude yet.
"""

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = PROJECT_ROOT / "Data" / "processed_chunks.json"
TOP_K = 3

DEFAULT_QUESTION = "Who owns Northbridge Industrial Components Ltd.?"

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "have", "in", "is", "it", "of", "on", "or", "that", "the",
    "this", "to", "was", "were", "what", "when", "where", "who", "why",
    "with", "does", "did", "do"
}

# These terms appear across the corpus and do not help distinguish sources.
CORPUS_COMMON_TERMS = {
    "northbridge", "industrial", "components", "ltd"
}

QUERY_EXPANSIONS = {
    "patched": "outdated software vulnerabilities remediation patching",
    "patch": "outdated software vulnerabilities remediation patching",
    "technology": "software system file-transfer service internet-facing",
    "externally": "internet-facing external exposed",
    "accessible": "internet-facing external exposed",
    "cybersecurity": "vulnerabilities breach exploitation remediation software",
    "cyber": "vulnerabilities breach exploitation remediation software",
    "sanctioned": "sanctions screening restrictive measures name match identifiers",
    "sanctions": "screening restrictive measures name match identifiers",
    "owned": "ownership shareholder beneficial owner registry",
    "owns": "ownership shareholder beneficial owner registry",
    "owner": "ownership shareholder beneficial owner registry",
}


def load_chunks(file_path: Path) -> list[dict]:
    """
    Load processed chunks from JSON.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Chunks file not found: {file_path}")

    chunks = json.loads(file_path.read_text(encoding="utf-8"))

    if not chunks:
        raise ValueError("Chunks file exists but contains no chunks.")

    return chunks


def expand_query(question: str) -> str:
    """
    Add domain-specific terms to improve retrieval for business-language questions.

    This is a simple, transparent form of query expansion.
    """
    tokens = re.findall(r"[a-zA-Z0-9]+", question.lower())
    expanded_terms = []

    for token in tokens:
        if token in QUERY_EXPANSIONS:
            expanded_terms.append(QUERY_EXPANSIONS[token])

    if expanded_terms:
        return question + " " + " ".join(expanded_terms)

    return question


def tokenize(text: str) -> list[str]:
    """
    Convert text into lowercase tokens and remove low-value words.
    """
    raw_tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())

    filtered_tokens = [
        token
        for token in raw_tokens
        if token not in STOPWORDS
        and token not in CORPUS_COMMON_TERMS
        and len(token) > 1
    ]

    return filtered_tokens


def build_term_vector(text: str) -> Counter:
    """
    Build a simple term-frequency vector from text.
    """
    return Counter(tokenize(text))


def cosine_similarity(vector_a: Counter, vector_b: Counter) -> float:
    """
    Calculate cosine similarity between two sparse term-frequency vectors.
    """
    common_terms = set(vector_a.keys()) & set(vector_b.keys())

    dot_product = sum(vector_a[term] * vector_b[term] for term in common_terms)

    magnitude_a = math.sqrt(sum(value * value for value in vector_a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_chunks(question: str, chunks: list[dict], top_k: int = TOP_K) -> list[dict]:
    """
    Rank chunks by similarity to the user question.
    """
    expanded_question = expand_query(question)
    question_vector = build_term_vector(expanded_question)
    scored_chunks = []

    for chunk in chunks:
        chunk_text = chunk["text"]
        chunk_vector = build_term_vector(chunk_text)
        score = cosine_similarity(question_vector, chunk_vector)

        scored_chunk = {
            **chunk,
            "similarity_score": score,
            "expanded_question": expanded_question,
        }

        scored_chunks.append(scored_chunk)

    ranked_chunks = sorted(
        scored_chunks,
        key=lambda item: item["similarity_score"],
        reverse=True,
    )

    return ranked_chunks[:top_k]


def print_results(question: str, results: list[dict]) -> None:
    """
    Print retrieved chunks in a readable format.
    """
    print("\nQuestion:")
    print(question)

    if results:
        expanded_question = results[0].get("expanded_question", question)
        if expanded_question != question:
            print("\nExpanded question:")
            print(expanded_question)

    print(f"\nTop {len(results)} retrieved chunks:\n")

    for rank, chunk in enumerate(results, start=1):
        print("=" * 80)
        print(f"Rank: {rank}")
        print(f"Similarity score: {chunk['similarity_score']:.4f}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source ID: {chunk['source_id']}")
        print(f"Source name: {chunk['source_name']}")
        print(f"Source date: {chunk['source_date']}")
        print(f"Source type: {chunk['source_type']}")
        print(f"Entity: {chunk['entity']}")
        print("\nText:")
        print(chunk["text"])
        print()


def main():
    """
    Run retrieval for a question.

    Usage:
    python3 Scripts/04_retrieve_chunks.py
    python3 Scripts/04_retrieve_chunks.py "Is Daniel Vermeer confirmed to be sanctioned?"
    """
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = DEFAULT_QUESTION

    chunks = load_chunks(CHUNKS_FILE)
    results = retrieve_chunks(question, chunks)
    print_results(question, results)


if __name__ == "__main__":
    main()