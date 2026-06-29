import json
import tempfile
from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import run_foundation_workflow
from reprobench.reporting import (
    benchmark_summary_to_dict,
    benchmark_summary_to_markdown,
    build_dashboard_html,
    report_to_dict,
    report_to_markdown,
    write_benchmark_summary,
    write_dashboard,
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

    def test_build_dashboard_html_contains_summary_and_findings(self):
        benchmark_summary = {
            "total_cases": 1,
            "matched_cases": 1,
            "cases": [
                {
                    "name": "data_leakage",
                    "expected_verdict": "partially_reproduced",
                    "actual_verdict": "partially_reproduced",
                    "matched": True,
                }
            ],
        }
        evidence_report = {
            "verdict": "partially_reproduced",
            "summary": "Metric reproduced with leakage warning.",
            "tool_calls": [{"name": "detect_data_leakage", "status": "completed"}],
            "findings": [
                {
                    "severity": "warning",
                    "title": "Potential target leakage",
                    "detail": "Feature copies target.",
                }
            ],
        }

        html = build_dashboard_html(benchmark_summary, evidence_report)

        self.assertIn("ReproBench Agent Demo Dashboard", html)
        self.assertIn("ReproBench Evidence Project", html)
        self.assertIn("Evidence Attachments", html)
        self.assertIn("Judging Evidence Matrix", html)
        self.assertIn("Potential target leakage", html)
        self.assertIn("detect_data_leakage", html)
        self.assertIn('data-label="Evidence"', html)

    def test_write_dashboard_writes_html_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            benchmark_path = root / "benchmark.json"
            report_path = root / "report.json"
            output_path = root / "dashboard" / "index.html"
            benchmark_path.write_text(
                json.dumps(
                    {
                        "total_cases": 1,
                        "matched_cases": 1,
                        "cases": [
                            {
                                "name": "clean_baseline",
                                "expected_verdict": "reproduced",
                                "actual_verdict": "reproduced",
                                "matched": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report_path.write_text(
                json.dumps(
                    {
                        "verdict": "reproduced",
                        "summary": "ok",
                        "tool_calls": [],
                        "findings": [],
                    }
                ),
                encoding="utf-8",
            )

            written = write_dashboard(benchmark_path, report_path, output_path)

            self.assertEqual(written, output_path)
            self.assertTrue(output_path.exists())
