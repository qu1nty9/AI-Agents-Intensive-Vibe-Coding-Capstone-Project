from pathlib import Path
from unittest import TestCase

from reprobench.benchmark import list_case_specs, load_case_spec, validate_all_cases
from reprobench.models import Verdict


class BenchmarkCasesTest(TestCase):
    def test_all_committed_cases_are_valid(self):
        results = validate_all_cases(Path("examples/cases"))

        self.assertEqual(len(results), 5)
        self.assertTrue(all(result.valid for result in results), results)

    def test_list_case_specs_returns_expected_suite(self):
        specs = list_case_specs(Path("examples/cases"))
        names = {spec.name for spec in specs}

        self.assertEqual(
            names,
            {
                "clean_baseline",
                "metric_mismatch",
                "seed_instability",
                "missing_dependency",
                "data_leakage",
            },
        )

    def test_data_leakage_case_contains_dataset_and_expected_verdict(self):
        spec = load_case_spec(Path("examples/cases/data_leakage"))

        self.assertEqual(spec.expected_verdict, Verdict.PARTIALLY_REPRODUCED)
        self.assertEqual(spec.target_column, "target")
        self.assertTrue(spec.dataset_path)
        self.assertTrue(spec.dataset_path.exists())
        self.assertIn("detect_data_leakage", spec.checks)

