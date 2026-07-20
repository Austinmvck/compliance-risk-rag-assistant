"""
Deterministic tests for the active sparse retrieval path.

These tests validate retrieval behavior without calling Claude or requiring
an Anthropic API key.
"""

import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RETRIEVAL_SCRIPT = PROJECT_ROOT / "Scripts" / "04_retrieve_chunks.py"
CHUNKS_FILE = PROJECT_ROOT / "Data" / "processed_chunks.json"

retrieval_module = SourceFileLoader(
    "sparse_retrieval_module",
    str(RETRIEVAL_SCRIPT),
).load_module()


class SparseRetrievalTests(unittest.TestCase):
    """Protect the highest-value deterministic retrieval behaviors."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.chunks = retrieval_module.load_chunks(CHUNKS_FILE)

    def retrieve(self, question: str) -> list[dict]:
        return retrieval_module.retrieve_chunks(question, self.chunks)

    def test_ownership_question_retrieves_registry_evidence(self) -> None:
        results = self.retrieve(
            "Who owns Northbridge Industrial Components Ltd.?"
        )

        source_names = {chunk["source_name"] for chunk in results}

        self.assertIn(
            "Corporate Registry Extract",
            source_names,
            "Ownership questions should retrieve corporate-registry evidence.",
        )

    def test_sanctions_question_retrieves_screening_evidence(self) -> None:
        results = self.retrieve("Is Daniel Vermeer sanctioned?")

        source_names = {chunk["source_name"] for chunk in results}

        self.assertIn(
            "Sanctions Screening Report",
            source_names,
            "Sanctions questions should retrieve sanctions-screening evidence.",
        )

    def test_patching_question_retrieves_conflicting_sources(self) -> None:
        results = self.retrieve("Are Northbridge systems fully patched?")

        source_names = {chunk["source_name"] for chunk in results}

        self.assertIn(
            "Vendor Questionnaire",
            source_names,
            "Patching questions should retrieve the vendor's self-report.",
        )
        self.assertIn(
            "Cybersecurity Monitoring Report",
            source_names,
            "Patching questions should retrieve later monitoring evidence.",
        )

    def test_unsupported_bribery_question_returns_no_evidence(self) -> None:
        results = self.retrieve(
            "Did Northbridge engage in bribery or corruption?"
        )

        self.assertEqual(
            [],
            results,
            "Unsupported allegations should not retrieve weak evidence above the threshold.",
        )

    def test_retrieved_chunks_include_required_provenance(self) -> None:
        results = self.retrieve(
            "Who owns Northbridge Industrial Components Ltd.?"
        )

        self.assertGreater(
            len(results),
            0,
            "The provenance test requires at least one retrieved result.",
        )

        required_fields = {
            "chunk_id",
            "source_id",
            "source_name",
            "source_date",
            "source_type",
            "entity",
            "text",
            "similarity_score",
            "expanded_question",
        }

        for chunk in results:
            missing_fields = required_fields - set(chunk)

            self.assertFalse(
                missing_fields,
                f"Retrieved chunk is missing fields: {sorted(missing_fields)}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
