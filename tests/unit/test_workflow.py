from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import build_initial_plan, run_foundation_workflow
from reprobench.models import Verdict


class WorkflowTest(TestCase):
    def test_build_initial_plan_contains_core_steps_and_safety_checks(self):
        plan = build_initial_plan(Path("examples/cases/clean_baseline"))

        self.assertEqual(plan.case_name, "clean_baseline")
        self.assertGreaterEqual(len(plan.steps), 5)
        self.assertIn("scan_for_secrets", plan.safety_checks)

    def test_foundation_workflow_returns_blocked_dry_run_report(self):
        report = run_foundation_workflow(Path("examples/cases/clean_baseline"))

        self.assertEqual(report.case_name, "clean_baseline")
        self.assertEqual(report.verdict, Verdict.BLOCKED)
        self.assertGreaterEqual(len(report.tool_calls), 3)
        self.assertTrue(report.summary)

