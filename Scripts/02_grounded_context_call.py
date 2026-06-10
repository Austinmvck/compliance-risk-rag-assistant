"""
Week 2: Controlled-context compliance risk analysis.

This script:
1. Reads a synthetic vendor case from a local file.
2. Sends the full source material to Claude.
3. Instructs Claude to use only the supplied evidence.
4. Requires a structured response with source references.
5. Tests uncertainty and human-review behavior.

This is controlled-context grounding, not full RAG.
"""

import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


# Find the repository root from the location of this script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load the API key from the project's local .env file.
load_dotenv(PROJECT_ROOT / ".env")

SOURCE_FILE = PROJECT_ROOT / "Data" / "sample_vendor_case.txt"

QUESTION = (
    "What compliance or operational risks are supported by the supplied evidence?"
)


def load_source_document(file_path: Path) -> str:
    """Load the controlled source document."""

    if not file_path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")

    source_text = file_path.read_text(encoding="utf-8").strip()

    if not source_text:
        raise ValueError(f"Source file is empty: {file_path}")

    return source_text


def build_prompt(source_text: str, question: str) -> str:
    """Build a prompt that restricts Claude to the supplied evidence."""

    return f"""
You are helping a compliance and third-party risk analyst review a vendor.

Answer the user question using only the SUPPLIED SOURCE MATERIAL below.

Rules:
- Do not use outside knowledge.
- Do not invent facts.
- Distinguish confirmed facts from possible risks.
- If the evidence does not support an answer, state "Insufficient evidence."
- If sources conflict, explain the conflict rather than deciding which is correct.
- Reference source labels exactly as written, such as SOURCE A or SOURCE B.
- Recommend human review when material questions remain unresolved.

Return the answer using this exact structure:

Risk finding:
Evidence used:
Source references:
Unknowns or conflicting information:
Confidence:
Human review required:

USER QUESTION:
{question}

SUPPLIED SOURCE MATERIAL:
{source_text}
""".strip()


def main():
    """
    Load the source document, send it to Claude, and print the response.

    PM concept:
    This tests whether the model can produce a source-grounded,
    traceable response before automated retrieval is introduced.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Add it to your .env file."
        )

    source_text = load_source_document(SOURCE_FILE)
    prompt = build_prompt(source_text, QUESTION)

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        print("\nGrounded compliance risk response:\n")
        print(message.content[0].text)

    except Exception as e:
        print("Error calling Claude API:")
        print(e)


if __name__ == "__main__":
    main()