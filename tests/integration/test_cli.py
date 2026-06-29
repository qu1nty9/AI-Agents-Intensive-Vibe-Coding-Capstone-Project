import subprocess
import sys
import tempfile
from unittest import TestCase


class CliTest(TestCase):
    def test_module_help_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Evidence-first agent", result.stdout)

    def test_info_command_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "info"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("ReproBench Agent", result.stdout)

    def test_cases_validate_command_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "cases", "validate"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Valid cases: 5/5", result.stdout)

    def test_cases_list_command_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "cases", "list"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("data_leakage", result.stdout)

    def test_cases_audit_command_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "cases", "audit"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Expected verdicts matched: 5/5", result.stdout)

    def test_cases_audit_command_writes_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "reprobench",
                    "cases",
                    "audit",
                    "--output-dir",
                    temp_dir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Wrote benchmark summary", result.stdout)

    def test_run_command_writes_report_bundle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "reprobench",
                    "run",
                    "examples/cases/data_leakage",
                    "--output-dir",
                    temp_dir,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Wrote report", result.stdout)

    def test_dashboard_command_writes_html(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "reprobench",
                    "dashboard",
                    "--output",
                    f"{temp_dir}/index.html",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Wrote demo dashboard", result.stdout)

    def test_mcp_list_tools_command_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "reprobench", "mcp", "list-tools"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("audit_case", result.stdout)

    def test_mcp_call_command_runs(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "reprobench",
                "mcp",
                "call",
                "audit_case",
                "--args-json",
                '{"case_path":"examples/cases/clean_baseline"}',
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn('"verdict": "reproduced"', result.stdout)
