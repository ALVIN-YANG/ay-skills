from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_product_evals", ROOT / "scripts" / "run_product_evals.py"
)
assert SPEC and SPEC.loader
product = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = product
SPEC.loader.exec_module(product)


class ProductEvalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rubric = {
            "minimum_median_total": 16,
            "minimum_win_rate": 0.7,
            "maximum_critical_failures": 0,
            "maximum_average_question_batches": 1.0,
            "dimensions": [
                {"id": f"d{index}", "description": "criterion"}
                for index in range(10)
            ],
            "critical_failures": [{"id": "fabricated", "description": "bad"}],
        }

    def evaluation(self, score: int = 2) -> dict[str, object]:
        scores = [
            {"id": f"d{index}", "score": score, "reason": "evidence"}
            for index in range(10)
        ]
        return {
            "total": score * 10,
            "dimension_scores": scores,
            "critical_failures": [],
            "question_batches": 0,
            "summary": "good",
        }

    def test_blind_order_is_deterministic_and_varies(self) -> None:
        values = [product.blind_order("case", repetition) for repetition in range(1, 20)]
        self.assertEqual(values, [product.blind_order("case", n) for n in range(1, 20)])
        self.assertIn(True, values)
        self.assertIn(False, values)

    def test_normalize_evaluation_accepts_exact_rubric(self) -> None:
        data = {
            "winner": "A",
            "reason": "better",
            "a": self.evaluation(2),
            "b": self.evaluation(1),
        }
        self.assertEqual(product.normalize_evaluation(data, self.rubric), [])

    def test_normalize_evaluation_recomputes_total_and_rejects_wrong_ids(self) -> None:
        bad = self.evaluation(2)
        bad["total"] = 3
        bad["dimension_scores"][0]["id"] = "wrong"  # type: ignore[index]
        data = {"winner": "tie", "reason": "same", "a": bad, "b": self.evaluation(2)}
        errors = product.normalize_evaluation(data, self.rubric)
        self.assertTrue(any("dimension ids" in error for error in errors))
        self.assertEqual(bad["total"], 20)

    def test_normalize_evaluation_derives_winner(self) -> None:
        data = {
            "winner": "B",
            "reason": "model arithmetic was wrong",
            "a": self.evaluation(2),
            "b": self.evaluation(1),
        }
        self.assertEqual(product.normalize_evaluation(data, self.rubric), [])
        self.assertEqual(data["winner"], "A")

    def test_summary_applies_quality_thresholds(self) -> None:
        results = [
            product.CaseResult("one", True, 18, 14, True, False, (), 0),
            product.CaseResult("two", True, 16, 16, False, True, (), 1),
            product.CaseResult("three", True, 17, 12, True, False, (), 1),
        ]
        summary, passed = product.summarize(results, self.rubric)
        self.assertTrue(passed)
        self.assertEqual(summary["median_skilled_score"], 17)
        self.assertGreaterEqual(summary["effective_win_rate"], 0.7)

    def test_summary_fails_on_critical_failure(self) -> None:
        result = product.CaseResult(
            "one", True, 20, 10, True, False, ("fabricated",), 0
        )
        _, passed = product.summarize([result], self.rubric)
        self.assertFalse(passed)


if __name__ == "__main__":
    unittest.main()
