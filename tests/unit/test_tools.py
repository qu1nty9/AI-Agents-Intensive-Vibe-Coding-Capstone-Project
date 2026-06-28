from pathlib import Path
from unittest import TestCase

from reprobench.models import Claim
from reprobench.tools import (
    classify_execution_error,
    compare_metric,
    detect_data_leakage,
    detect_missing_seed,
    parse_last_json_object,
    run_python_script,
)


class ToolsTest(TestCase):
    def test_parse_last_json_object(self):
        parsed = parse_last_json_object('noise\n{"metric_name": "accuracy", "value": 0.9}\n')

        self.assertEqual(parsed, {"metric_name": "accuracy", "value": 0.9})

    def test_compare_metric_passes_within_tolerance(self):
        comparison = compare_metric(
            Claim(metric_name="accuracy", expected_value=0.9, tolerance=0.01),
            {"metric_name": "accuracy", "value": 0.905},
        )

        self.assertTrue(comparison.passed)

    def test_run_python_script_parses_metric_output(self):
        result = run_python_script(Path("examples/cases/clean_baseline/experiment.py"))

        self.assertEqual(result.return_code, 0)
        self.assertEqual(result.parsed_output["metric_name"], "accuracy")
        self.assertEqual(result.parsed_output["value"], 0.9)

    def test_detect_missing_seed_flags_seed_instability_case(self):
        findings = detect_missing_seed(Path("examples/cases/seed_instability/experiment.py"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].title, "Missing seed control")

    def test_detect_data_leakage_flags_target_copy(self):
        findings = detect_data_leakage(
            Path("examples/cases/data_leakage/toy_leakage.csv"),
            "target",
        )

        self.assertTrue(any(finding.title == "Potential target leakage" for finding in findings))

    def test_classify_execution_error_detects_missing_dependency(self):
        result = run_python_script(Path("examples/cases/missing_dependency/experiment.py"))
        findings = classify_execution_error(result)

        self.assertEqual(result.return_code, 1)
        self.assertEqual(findings[0].title, "Missing dependency")

