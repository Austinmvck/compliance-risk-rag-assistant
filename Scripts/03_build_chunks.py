"""
Week 3: Build retrievable source chunks.

This script:
1. Reads source documents from Data/sources.
2. Extracts source-level metadata.
3. Splits each document into smaller text chunks.
4. Preserves metadata on every chunk.
5. Saves the chunks to Data/processed_chunks.json.

This prepares the project for retrieval, but does not perform retrieval yet.
"""

import json
from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = PROJECT_ROOT / "Data" / "sources"
OUTPUT_FILE = PROJECT_ROOT / "Data" / "processed_chunks.json"

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120


def parse_source_file(file_path: Path) -> dict:
    """
    Parse a source file into metadata and content.

    Expected source file format:
    SOURCE_ID: ...
    SOURCE_NAME: ...
    SOURCE_DATE: ...
    SOURCE_TYPE: ...
    ENTITY: ...

    CONTENT:
    ...
    """
    text = file_path.read_text(encoding="utf-8").strip()

    if "CONTENT:" not in text:
        raise ValueError(f"Missing CONTENT section in {file_path}")

    metadata_text, content = text.split("CONTENT:", maxsplit=1)

    metadata = {}

    for line in metadata_text.strip().splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", maxsplit=1)
        metadata[key.strip().lower()] = value.strip()

    required_fields = [
        "source_id",
        "source_name",
        "source_date",
        "source_type",
        "entity",
    ]

    missing_fields = [field for field in required_fields if not metadata.get(field)]

    if missing_fields:
        raise ValueError(f"{file_path} missing metadata fields: {missing_fields}")

    metadata["file_name"] = file_path.name
    metadata["content"] = content.strip()

    return metadata


def split_into_sentences(text):
    """
    Split text into sentences using a lightweight regex approach.

    This avoids adding new dependencies while keeping sentence boundaries
    more intact than raw character-based chunking.
    """
    normalized_text = re.sub(r"\s+", " ", text).strip()
    if not normalized_text:
        return []

    return re.split(r"(?<=[.!?])\s+(?=[A-Z])", normalized_text)


def chunk_text(text, chunk_size=CHUNK_SIZE):
    """
    Group full sentences into chunks up to the target chunk size.

    This keeps facts and qualifiers together more often than character-based
    chunking, which can split words or cut claims in half.
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        candidate = " ".join(current_chunk + [sentence]).strip()

        if len(candidate) <= chunk_size:
            current_chunk.append(sentence)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk).strip())
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks


def build_chunks() -> list[dict]:
    """
    Build chunk records from all .txt files in the source directory.
    """
    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"Source directory not found: {SOURCE_DIR}")

    source_files = sorted(SOURCE_DIR.glob("*.txt"))

    if not source_files:
        raise FileNotFoundError(f"No .txt source files found in {SOURCE_DIR}")

    all_chunks = []

    for source_file in source_files:
        source = parse_source_file(source_file)
        text_chunks = chunk_text(source["content"])

        for index, chunk in enumerate(text_chunks, start=1):
            chunk_record = {
                "chunk_id": f"{source['source_id']}_CHUNK_{index}",
                "source_id": source["source_id"],
                "source_name": source["source_name"],
                "source_date": source["source_date"],
                "source_type": source["source_type"],
                "entity": source["entity"],
                "file_name": source["file_name"],
                "chunk_index": index,
                "text": chunk,
            }

            all_chunks.append(chunk_record)

    return all_chunks


def save_chunks(chunks: list[dict]) -> None:
    """
    Save chunk records to JSON.
    """
    OUTPUT_FILE.write_text(
        json.dumps(chunks, indent=2),
        encoding="utf-8",
    )


def main():
    chunks = build_chunks()
    save_chunks(chunks)

    print(f"Built {len(chunks)} chunks from source documents.")
    print(f"Saved chunks to: {OUTPUT_FILE}")

    print("\nChunk preview:\n")

    for chunk in chunks:
        print("-" * 80)
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(f"Source: {chunk['source_name']}")
        print(f"Date: {chunk['source_date']}")
        print(f"Type: {chunk['source_type']}")
        print(f"Entity: {chunk['entity']}")
        print(f"Text preview: {chunk['text'][:300]}")


if __name__ == "__main__":
    main()