"""
Hybrid retrieval experiment using Reciprocal Rank Fusion (RRF).

Purpose:
- Compare sparse retrieval and semantic retrieval without averaging raw scores.
Sparse lexical retrieval scores and semantic embedding cosine scores are on different scales. - RRF combines ranked results from both retrieval methods.
This script is experimental and does not feed Claude directly.
The current generation path remains Scripts/05_rag_answer.py using sparse retrieval.
"""

import importlib.util
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).resolve().parents[1]
CHUNKS_PATH = ROOT_DIR / "Data" / "processed_chunks.json"
SPARSE_SCRIPT_PATH = ROOT_DIR / "Scripts" / "04_retrieve_chunks.py"

SEMANTIC_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SEMANTIC_MIN_SIMILARITY_SCORE = 0.20
RRF_K = 60
TOP_K = 5


def load_sparse_module():
    """
    Load Scripts/04_retrieve_chunks.py by file path.

    The file name starts with a number, so it cannot be imported with a normal
    Python import statement.
    """
    spec = importlib.util.spec_from_file_location(
        "sparse_retrieve_chunks",
        SPARSE_SCRIPT_PATH,
    )
    sparse_module = importlib.util.module_from_spec(spec)

    if spec.loader is None:
        raise ImportError(f"Could not load sparse retrieval module from {SPARSE_SCRIPT_PATH}")

    spec.loader.exec_module(sparse_module)
    return sparse_module


def load_chunks() -> List[Dict]:
    """Load processed source chunks."""
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_PATH}. Run Scripts/03_build_chunks.py first."
        )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)

    if denominator == 0:
        return 0.0

    return float(np.dot(vector_a, vector_b) / denominator)


def semantic_retrieve_chunks(question: str, chunks: List[Dict], top_k: int = TOP_K) -> List[Tuple[Dict, float]]:
    """
    Retrieve chunks using semantic embedding similarity.

    Returns:
        List of tuples: (chunk, semantic_score)
    """
    model = SentenceTransformer(SEMANTIC_MODEL_NAME)

    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = model.encode(chunk_texts, convert_to_numpy=True)
    question_embedding = model.encode(question, convert_to_numpy=True)

    scored_chunks = []

    for chunk, chunk_embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(question_embedding, chunk_embedding)

        if score >= SEMANTIC_MIN_SIMILARITY_SCORE:
            scored_chunks.append((chunk, score))

    scored_chunks.sort(key=lambda item: item[1], reverse=True)

    return scored_chunks[:top_k]


def chunk_key(chunk: Dict) -> str:
    """Create a stable key for combining sparse and semantic results."""
    return chunk.get("chunk_id", chunk.get("id", chunk.get("text", "")))


def unpack_result(result):
    """
    Normalize sparse and semantic retrieval result shapes.

    The semantic retriever returns tuples shaped like:
        (chunk, score)

    The sparse retriever may return tuples with more than two values or
    dictionaries, depending on the existing implementation. For hybrid ranking,
    we only need the chunk and the original method score.
    """
    if isinstance(result, tuple):
        chunk = result[0]
        original_score = result[1] if len(result) > 1 else None
        return chunk, original_score

    if isinstance(result, dict):
        chunk = result.get("chunk", result)
        original_score = (
            result.get("score")
            or result.get("similarity_score")
            or result.get("sparse_score")
            or result.get("semantic_score")
        )
        return chunk, original_score

    raise ValueError(f"Unsupported retrieval result format: {type(result)}")


def reciprocal_rank_fusion(
    sparse_results: List,
    semantic_results: List,
    top_k: int = TOP_K,
) -> List[Dict]:
    """
    Combine sparse and semantic retrieval results using Reciprocal Rank Fusion.

    RRF formula:
        score += 1 / (RRF_K + rank)

    Rank starts at 1.
    """
    combined: Dict[str, Dict] = {}

    def add_results(results: List, method_name: str) -> None:
        for rank, result in enumerate(results, start=1):
            chunk, original_score = unpack_result(result)
            key = chunk_key(chunk)

            if key not in combined:
                combined[key] = {
                    "chunk": chunk,
                    "rrf_score": 0.0,
                    "sparse_rank": None,
                    "semantic_rank": None,
                    "sparse_score": None,
                    "semantic_score": None,
                }

            combined[key]["rrf_score"] += 1 / (RRF_K + rank)

            if method_name == "sparse":
                combined[key]["sparse_rank"] = rank
                combined[key]["sparse_score"] = original_score

            if method_name == "semantic":
                combined[key]["semantic_rank"] = rank
                combined[key]["semantic_score"] = original_score

    add_results(sparse_results, "sparse")
    add_results(semantic_results, "semantic")

    fused_results = list(combined.values())
    fused_results.sort(key=lambda item: item["rrf_score"], reverse=True)

    return fused_results[:top_k]


def print_results(question: str, fused_results: List[Dict]) -> None:
    """Print hybrid retrieval results."""
    print("\n=== Hybrid Retrieval Experiment ===")
    print(f"Question: {question}")
    print("Retrieval method: Reciprocal Rank Fusion over sparse + semantic")
    print(f"RRF k: {RRF_K}")
    print(f"Semantic threshold: {SEMANTIC_MIN_SIMILARITY_SCORE}")
    print(f"Top k: {TOP_K}")

    if not fused_results:
        print("\nNo relevant hybrid evidence retrieved.")
        return

    print("\nTop hybrid results:")

    for index, result in enumerate(fused_results, start=1):
        chunk = result["chunk"]

        print("\n" + "-" * 80)
        print(f"Rank {index}")
        print(f"Chunk ID: {chunk.get('chunk_id', 'N/A')}")
        print(f"Source ID: {chunk.get('source_id', 'N/A')}")
        print(f"Source Name: {chunk.get('source_name', 'N/A')}")
        print(f"Source Type: {chunk.get('source_type', 'N/A')}")
        print(f"Source Date: {chunk.get('source_date', 'N/A')}")
        print(f"RRF Score: {result['rrf_score']:.6f}")
        print(f"Sparse Rank: {result['sparse_rank']}")
        print(f"Sparse Score: {result['sparse_score']}")
        print(f"Semantic Rank: {result['semantic_rank']}")
        print(f"Semantic Score: {result['semantic_score']}")
        print("\nText:")
        print(chunk.get("text", "").strip())


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 Scripts/07_hybrid_retrieve_chunks.py '<question>'")
        sys.exit(1)

    question = sys.argv[1]

    sparse_module = load_sparse_module()
    chunks = load_chunks()

    sparse_results = sparse_module.retrieve_chunks(question, chunks, top_k=TOP_K)
    semantic_results = semantic_retrieve_chunks(question, chunks, top_k=TOP_K)

    fused_results = reciprocal_rank_fusion(
        sparse_results=sparse_results,
        semantic_results=semantic_results,
        top_k=TOP_K,
    )

    print_results(question, fused_results)


if __name__ == "__main__":
    main()