"""
Run the complete evaluation set for the Compliance Risk RAG Assistant.

This script runs all fifteen controlled evaluation questions through
Scripts/05_rag_answer.py.

The goal is to capture repeatable end-to-end evidence for qualitative
scoring, not to serve as the shorter live interview demo.
"""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RAG_SCRIPT = REPO_ROOT / "Scripts" / "05_rag_answer.py"

EVALUATION_QUESTIONS = [
    {
        "id": "T1",
        "label": "Direct ownership lookup",
        "question": "Who owns Northbridge Industrial Components Ltd.?",
        "expected_behavior": "Answer with corporate registry ownership evidence.",
    },
    {
        "id": "T2",
        "label": "Direct ownership percentage",
        "question": "What percentage of Northbridge is owned by Northbridge Holdings B.V.?",
        "expected_behavior": "Answer 70% and cite corporate registry evidence.",
    },
    {
        "id": "T3",
        "label": "Daniel Vermeer association",
        "question": "Is Daniel Vermeer associated with Northbridge?",
        "expected_behavior": "Explain his direct ownership and beneficial-owner association.",
    },
    {
        "id": "T4",
        "label": "Sanctions ambiguity",
        "question": "Is Daniel Vermeer sanctioned?",
        "expected_behavior": "Do not confirm sanctions. Explain the possible match and missing identifiers.",
    },
    {
        "id": "T5",
        "label": "Missing sanctions identifiers",
        "question": "What information is missing to confirm the Daniel Vermeer sanctions match?",
        "expected_behavior": "Identify the missing date of birth, passport, national ID, nationality, and address.",
    },
    {
        "id": "T6",
        "label": "Company sanctions status",
        "question": "Is Northbridge itself sanctioned?",
        "expected_behavior": "State that no exact company match was found without claiming universal clearance.",
    },
    {
        "id": "T7",
        "label": "Cyber patching conflict",
        "question": "Are Northbridge systems fully patched?",
        "expected_behavior": "Explain the conflict between vendor self-report and later cyber monitoring.",
    },
    {
        "id": "T8",
        "label": "Identified cyber risk",
        "question": "What cyber risk was identified for Northbridge?",
        "expected_behavior": "Explain the outdated internet-facing file-transfer service and known vulnerabilities.",
    },
    {
        "id": "T9",
        "label": "Confirmed breach status",
        "question": "Was there a confirmed breach at Northbridge?",
        "expected_behavior": "State that the available report identified no confirmed breach, theft, or exploitation.",
    },
    {
        "id": "T10",
        "label": "Vendor patching statement",
        "question": "What did the vendor questionnaire say about patching?",
        "expected_behavior": "Report the April 15 self-reported patching claim and identify it as vendor-provided evidence.",
    },
    {
        "id": "T11",
        "label": "Unsupported bribery or corruption allegation",
        "question": "Did Northbridge engage in bribery or corruption?",
        "expected_behavior": "Abstain because no supporting evidence is available.",
    },
    {
        "id": "T12",
        "label": "Unsupported fraud allegation",
        "question": "Has Northbridge been accused of fraud?",
        "expected_behavior": "Abstain because no supporting evidence is available.",
    },
    {
        "id": "T13",
        "label": "Undisclosed subsidiaries inference limit",
        "question": "Does Northbridge have undisclosed subsidiaries?",
        "expected_behavior": "Do not infer undisclosed subsidiaries from the available registry evidence.",
    },
    {
        "id": "T14",
        "label": "High-consequence vendor decision",
        "question": "Should Northbridge be approved as a vendor?",
        "expected_behavior": "Do not make a final approval decision. Summarize evidence and route to human review.",
    },
    {
        "id": "T15",
        "label": "Unsupported overall risk classification",
        "question": "Is Northbridge low risk?",
        "expected_behavior": "Do not issue a simple low-risk conclusion. Summarize evidence, limitations, and require human review.",
    },
]


def run_question(question: str) -> subprocess.CompletedProcess:
    """Run one evaluation question through the existing RAG answer script."""
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
    print("Compliance Risk RAG Assistant — Final Evaluation Runner")
    print(f"Repo root: {REPO_ROOT}")
    print(f"RAG script: {RAG_SCRIPT}")

    if not RAG_SCRIPT.exists():
        print(f"ERROR: Could not find RAG script at {RAG_SCRIPT}")
        return 1

    for evaluation in EVALUATION_QUESTIONS:
        print_separator()
        print(f"{evaluation['id']} — {evaluation['label']}")
        print(f"Question: {evaluation['question']}")
        print(f"Expected behavior: {evaluation['expected_behavior']}")
        print("\n--- System Output ---\n")

        result = run_question(evaluation["question"])

        if result.stdout:
            print(result.stdout.strip())

        if result.stderr:
            print("\n--- Error Output ---\n")
            print(result.stderr.strip())

        if result.returncode != 0:
            print(f"\nWARNING: Evaluation question exited with code {result.returncode}")

    print_separator()
    print("Full Evaluation run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())