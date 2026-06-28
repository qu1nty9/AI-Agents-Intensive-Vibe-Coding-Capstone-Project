import json
import tempfile
from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import run_foundation_workflow
from reprobench.reporting import report_to_dict, report_to_markdown, write_report_bundle


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

