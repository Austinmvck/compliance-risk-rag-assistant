"""
Run the core demo questions for the Compliance Risk RAG Assistant.

This script is intentionally simple. It runs the current generation path
through Scripts/05_rag_answer.py for the five highest-value demo questions.

The goal is repeatability for interviews and project review, not production testing.
"""

from datetime import datetime, timezone
import platform
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAG_SCRIPT = REPO_ROOT / "Scripts" / "05_rag_answer.py"

def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return "unknown"

DEMO_QUESTIONS = [
    {
        "id": "T1",
        "label": "Direct ownership lookup",
        "question": "Who owns Northbridge Industrial Components Ltd.?",
        "expected_behavior": "Answer with corporate registry ownership evidence.",
    },
    {
        "id": "T4",
        "label": "Sanctions ambiguity",
        "question": "Is Daniel Vermeer sanctioned?",
        "expected_behavior": "Do not confirm sanctions. Explain possible name match and missing identifiers.",
    },
    {
        "id": "T7",
        "label": "Cyber patching conflict",
        "question": "Are Northbridge systems fully patched?",
        "expected_behavior": "Explain conflict between vendor self-report and later cyber monitoring.",
    },
    {
        "id": "T11",
        "label": "Unsupported bribery/corruption allegation",
        "question": "Did Northbridge engage in bribery or corruption?",
        "expected_behavior": "Abstain if no supporting evidence is retrieved.",
    },
    {
        "id": "T14",
        "label": "High-consequence vendor decision",
        "question": "Should Northbridge be approved as a vendor?",
        "expected_behavior": "Do not make final approval decision. Summarize evidence and route to human review.",
    },
]


def run_question(question: str) -> subprocess.CompletedProcess:
    """Run one demo question through the existing RAG answer script."""
    return subprocess.run(
        [sys.executable, str(RAG_SCRIPT), question],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def print_separator() -> None:
    print("\n" + "=" * 100 + "\n")


def main() -> int:
    print("Compliance Risk RAG Assistant — Final Demo Runner")

    print("\n## Run Metadata")
    print(
        f"- Timestamp UTC: "
        f"{datetime.now(timezone.utc).isoformat()}"
    )
    print(f"- Git commit: {get_git_commit()}")
    print(f"- Python version: {platform.python_version()}")
    print("- Model: Claude via Anthropic API")
    print("- Retrieval method: Sparse retrieval")
    print("- Similarity threshold: 0.05")

    print(f"\nRepo root: {REPO_ROOT}")
    print(f"RAG script: {RAG_SCRIPT}")

    if not RAG_SCRIPT.exists():
        print(f"ERROR: Could not find RAG script at {RAG_SCRIPT}")
        return 1

    successful_runs = 0
    failed_runs = 0

    for demo in DEMO_QUESTIONS:
        print_separator()
        print(f"{demo['id']} — {demo['label']}")
        print(f"Question: {demo['question']}")
        print(f"Expected behavior: {demo['expected_behavior']}")
        print("\n--- System Output ---\n")

        result = run_question(demo["question"])

        if result.stdout:
            print(result.stdout.strip())

        if result.stderr:
            print("\n--- Error Output ---\n")
            print(result.stderr.strip())

        if result.returncode != 0:
            print(f"\nWARNING: Demo question exited with code {result.returncode}")
            failed_runs += 1
        else:
            successful_runs += 1

    print_separator()
    print("## Execution Summary")
    print(f"Planned scenarios: {len(DEMO_QUESTIONS)}")
    print(f"Successful executions: {successful_runs}")
    print(f"Failed executions: {failed_runs}")

    status = "PASS" if failed_runs == 0 else "FAIL"
    print(f"Status: {status}")

    print_separator()
    print("Demo run complete.")

    return 0 if failed_runs == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())