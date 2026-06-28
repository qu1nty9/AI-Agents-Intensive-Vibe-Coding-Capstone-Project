import subprocess
import sys
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
