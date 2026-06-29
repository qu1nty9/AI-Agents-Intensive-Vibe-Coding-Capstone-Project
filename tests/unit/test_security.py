import json
import tempfile
from pathlib import Path
from unittest import TestCase

from reprobench.agents.workflow import run_foundation_workflow
from reprobench.benchmark import CaseSpecError, load_case_spec
from reprobench.security import REDACTION_MARKER, redact_text
from reprobench.tools import run_python_script


class SecurityTest(TestCase):
    def test_redact_text_masks_secret_like_values(self):
        text = "api_key='1234567890abcdef'"

        self.assertEqual(redact_text(text), REDACTION_MARKER)

    def test_run_python_script_redacts_stdout_and_parsed_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "secret_output.py"
            script_path.write_text(
                "import json\n"
                "print(json.dumps({'metric_name': 'token', "
                "'value': 'sk-abcdefghijklmnopqrstuvwxyz'}))\n",
                encoding="utf-8",
            )

            result = run_python_script(script_path)

            self.assertEqual(result.return_code, 0)
            self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz", result.stdout)
            self.assertEqual(result.parsed_output["value"], REDACTION_MARKER)

    def test_case_spec_rejects_artifact_path_escape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            case_dir = root / "escape_case"
            case_dir.mkdir()
            outside_artifact = root / "outside.py"
            outside_artifact.write_text("print('unsafe')\n", encoding="utf-8")
            (case_dir / "case.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "name": "escape_case",
                        "artifact": "../outside.py",
                        "claim": {"metric_name": "accuracy", "expected_value": 1.0},
                        "expected_verdict": "unsafe_to_run",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(CaseSpecError):
                load_case_spec(case_dir)

    def test_workflow_trace_includes_path_policy_check(self):
        report = run_foundation_workflow(Path("examples/cases/clean_baseline"))
        tool_names = [tool_call.name for tool_call in report.tool_calls]

        self.assertIn("validate_path_policy", tool_names)
