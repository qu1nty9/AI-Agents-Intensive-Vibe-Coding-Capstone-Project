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

