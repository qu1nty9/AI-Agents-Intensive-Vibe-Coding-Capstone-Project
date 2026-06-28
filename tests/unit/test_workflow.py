from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import build_initial_plan, run_foundation_workflow
from reprobench.benchmark import list_case_specs
from reprobench.models import Verdict


class WorkflowTest(TestCase):
    def test_build_initial_plan_contains_core_steps_and_safety_checks(self):
        plan = build_initial_plan(Path("examples/cases/clean_baseline"))

        self.assertEqual(plan.case_name, "clean_baseline")
        self.assertGreaterEqual(len(plan.steps), 5)
        self.assertIn("scan_for_secrets", plan.safety_checks)

    def test_foundation_workflow_reproduces_clean_baseline(self):
        report = run_foundation_workflow(Path("examples/cases/clean_baseline"))

        self.assertEqual(report.case_name, "clean_baseline")
        self.assertEqual(report.verdict, Verdict.REPRODUCED)
        self.assertGreaterEqual(len(report.tool_calls), 3)
        self.assertTrue(report.summary)

    def test_all_case_verdicts_match_expected_verdicts(self):
        for spec in list_case_specs(Path("examples/cases")):
            with self.subTest(case=spec.name):
                report = run_foundation_workflow(spec.path)

                self.assertEqual(report.verdict, spec.expected_verdict)
