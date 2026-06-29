import json
import tempfile
from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import run_foundation_workflow
from reprobench.reporting import (
    benchmark_summary_to_dict,
    benchmark_summary_to_markdown,
    report_to_dict,
    report_to_markdown,
    write_benchmark_summary,
    write_report_bundle,
)


class ReportingTest(TestCase):
    def test_report_to_dict_contains_verdict_and_trace(self):
        report = run_foundation_workflow(Path("examples/cases/clean_baseline"))
        serialized = report_to_dict(report)

        self.assertEqual(serialized["verdict"], "reproduced")
        self.assertTrue(serialized["tool_calls"])

    def test_report_to_markdown_contains_findings(self):
        report = run_foundation_workflow(Path("examples/cases/data_leakage"))
        markdown = report_to_markdown(report)

        self.assertIn("ReproBench Evidence Report", markdown)
        self.assertIn("Potential target leakage", markdown)
        self.assertIn("partially_reproduced", markdown)

    def test_write_report_bundle_writes_markdown_and_json(self):
        report = run_foundation_workflow(Path("examples/cases/metric_mismatch"))
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path, json_path = write_report_bundle(report, Path(temp_dir))

            self.assertTrue(markdown_path.exists())
            self.assertTrue(json_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["verdict"], "not_reproduced")

    def test_benchmark_summary_serializes_match_rate(self):
        rows = [
            {
                "name": "clean_baseline",
                "expected_verdict": "reproduced",
                "actual_verdict": "reproduced",
                "matched": True,
            }
        ]

        payload = benchmark_summary_to_dict(rows)
        markdown = benchmark_summary_to_markdown(rows)

        self.assertEqual(payload["match_rate"], 1.0)
        self.assertIn("Expected verdicts matched", markdown)

    def test_write_benchmark_summary_writes_files(self):
        rows = [
            {
                "name": "metric_mismatch",
                "expected_verdict": "not_reproduced",
                "actual_verdict": "not_reproduced",
                "matched": True,
            }
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            markdown_path, json_path = write_benchmark_summary(rows, Path(temp_dir))

            self.assertTrue(markdown_path.exists())
            self.assertTrue(json_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["matched_cases"], 1)
