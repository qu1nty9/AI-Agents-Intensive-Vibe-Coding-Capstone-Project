import json
import tempfile
from pathlib import Path
from unittest import TestCase

from reprobench.mcp_server.json_stdio import handle_request
from reprobench.mcp_server.tools import call_tool, list_tools


class McpToolsTest(TestCase):
    def test_list_tools_exposes_core_contracts(self):
        tools = list_tools()
        names = {tool["name"] for tool in tools}

        self.assertIn("inspect_case", names)
        self.assertIn("audit_case", names)
        self.assertIn("detect_leakage", names)
        self.assertIn("export_case_report", names)

    def test_audit_case_tool_returns_expected_verdict(self):
        result = call_tool("audit_case", {"case_path": "examples/cases/data_leakage"})

        self.assertEqual(result["case_name"], "data_leakage")
        self.assertEqual(result["verdict"], "partially_reproduced")

    def test_compare_claim_metric_tool(self):
        result = call_tool(
            "compare_claim_metric",
            {
                "metric_name": "accuracy",
                "expected_value": 0.9,
                "actual_value": 0.91,
                "tolerance": 0.02,
            },
        )

        self.assertTrue(result["passed"])

    def test_export_case_report_tool_writes_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = call_tool(
                "export_case_report",
                {
                    "case_path": "examples/cases/metric_mismatch",
                    "output_dir": temp_dir,
                },
            )

            self.assertTrue(Path(result["markdown_path"]).exists())
            self.assertTrue(Path(result["json_path"]).exists())
            self.assertEqual(result["report"]["verdict"], "not_reproduced")

    def test_json_stdio_handles_tool_list_request(self):
        response = handle_request(json.dumps({"id": 1, "method": "tools/list"}))

        self.assertEqual(response["id"], 1)
        self.assertIn("tools", response["result"])

    def test_json_stdio_handles_tool_call_request(self):
        response = handle_request(
            json.dumps(
                {
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "inspect_case",
                        "arguments": {"case_path": "examples/cases/clean_baseline"},
                    },
                }
            )
        )

        self.assertEqual(response["id"], 2)
        self.assertEqual(response["result"]["name"], "clean_baseline")

