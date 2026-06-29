"""MCP-facing tool registry for ReproBench.

The registry is dependency-free so tests and CLI demos can exercise the same
contracts that the optional FastMCP server exposes when the MCP SDK is present.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from reprobench.benchmark import load_case_spec
from reprobench.reporting import report_to_dict, write_report_bundle
from reprobench.tools import (
    compare_metric,
    detect_data_leakage,
    detect_missing_seed,
    run_python_script,
    scan_for_secrets,
)
from reprobench.models import Claim
from reprobench.agents.workflow import run_foundation_workflow

ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    """Public schema for an MCP-exposed tool."""

    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler

    def public_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


def list_tools() -> list[dict[str, Any]]:
    """Return public MCP tool metadata."""

    return [tool.public_dict() for tool in TOOL_REGISTRY.values()]


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call a registered tool by name."""

    if name not in TOOL_REGISTRY:
        available = ", ".join(sorted(TOOL_REGISTRY))
        raise KeyError(f"unknown tool: {name}; available tools: {available}")
    return TOOL_REGISTRY[name].handler(arguments or {})


def inspect_case(arguments: dict[str, Any]) -> dict[str, Any]:
    spec = load_case_spec(Path(_required(arguments, "case_path")))
    claim = spec.claim
    return {
        "name": spec.name,
        "title": spec.title,
        "description": spec.description,
        "artifact_path": str(spec.artifact_path) if spec.artifact_path else None,
        "dataset_path": str(spec.dataset_path) if spec.dataset_path else None,
        "target_column": spec.target_column,
        "expected_verdict": spec.expected_verdict.value if spec.expected_verdict else None,
        "failure_mode": spec.failure_mode,
        "tags": list(spec.tags),
        "checks": list(spec.checks),
        "claim": {
            "metric_name": claim.metric_name,
            "expected_value": claim.expected_value,
            "tolerance": claim.tolerance,
            "source": claim.source,
        }
        if claim
        else None,
    }


def audit_case(arguments: dict[str, Any]) -> dict[str, Any]:
    report = run_foundation_workflow(Path(_required(arguments, "case_path")))
    return report_to_dict(report)


def run_case_artifact(arguments: dict[str, Any]) -> dict[str, Any]:
    result = run_python_script(
        Path(_required(arguments, "script_path")),
        timeout_seconds=int(arguments.get("timeout_seconds", 120)),
    )
    return {
        "command": list(result.command),
        "return_code": result.return_code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "duration_seconds": result.duration_seconds,
        "timed_out": result.timed_out,
        "parsed_output": result.parsed_output,
    }


def compare_claim_metric(arguments: dict[str, Any]) -> dict[str, Any]:
    claim = Claim(
        metric_name=str(_required(arguments, "metric_name")),
        expected_value=float(_required(arguments, "expected_value")),
        tolerance=float(arguments.get("tolerance", 0.0)),
    )
    observed = {
        "metric_name": str(arguments.get("observed_metric_name", claim.metric_name)),
        "value": float(_required(arguments, "actual_value")),
    }
    comparison = compare_metric(claim, observed)
    return {
        "metric_name": comparison.metric_name,
        "expected_value": comparison.expected_value,
        "actual_value": comparison.actual_value,
        "tolerance": comparison.tolerance,
        "delta": comparison.delta,
        "passed": comparison.passed,
    }


def detect_seed_issue(arguments: dict[str, Any]) -> dict[str, Any]:
    findings = detect_missing_seed(Path(_required(arguments, "script_path")))
    return {"findings": [_finding_to_dict(finding) for finding in findings]}


def detect_leakage(arguments: dict[str, Any]) -> dict[str, Any]:
    findings = detect_data_leakage(
        Path(_required(arguments, "dataset_path")),
        str(_required(arguments, "target_column")),
    )
    return {"findings": [_finding_to_dict(finding) for finding in findings]}


def scan_case_for_secrets(arguments: dict[str, Any]) -> dict[str, Any]:
    findings = scan_for_secrets(Path(_required(arguments, "path")))
    return {"findings": [_finding_to_dict(finding) for finding in findings]}


def export_case_report(arguments: dict[str, Any]) -> dict[str, Any]:
    report = run_foundation_workflow(Path(_required(arguments, "case_path")))
    markdown_path, json_path = write_report_bundle(report, Path(_required(arguments, "output_dir")))
    return {
        "markdown_path": str(markdown_path),
        "json_path": str(json_path),
        "report": report_to_dict(report),
    }


def _required(arguments: dict[str, Any], key: str) -> Any:
    if key not in arguments or arguments[key] in (None, ""):
        raise ValueError(f"missing required argument: {key}")
    return arguments[key]


def _finding_to_dict(finding) -> dict[str, str]:
    return {
        "severity": finding.severity,
        "title": finding.title,
        "detail": finding.detail,
    }


def _schema(properties: dict[str, dict[str, Any]], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


TOOL_REGISTRY: dict[str, ToolSpec] = {
    "inspect_case": ToolSpec(
        name="inspect_case",
        description="Load and return normalized metadata for a ReproBench benchmark case.",
        input_schema=_schema(
            {"case_path": {"type": "string", "description": "Path to a benchmark case directory."}},
            ["case_path"],
        ),
        handler=inspect_case,
    ),
    "audit_case": ToolSpec(
        name="audit_case",
        description="Run the ReproBench audit workflow for a benchmark case.",
        input_schema=_schema(
            {"case_path": {"type": "string", "description": "Path to a benchmark case directory."}},
            ["case_path"],
        ),
        handler=audit_case,
    ),
    "run_case_artifact": ToolSpec(
        name="run_case_artifact",
        description="Run a Python experiment artifact and parse JSON metric output.",
        input_schema=_schema(
            {
                "script_path": {"type": "string"},
                "timeout_seconds": {"type": "integer", "default": 120},
            },
            ["script_path"],
        ),
        handler=run_case_artifact,
    ),
    "compare_claim_metric": ToolSpec(
        name="compare_claim_metric",
        description="Compare expected and observed metric values within tolerance.",
        input_schema=_schema(
            {
                "metric_name": {"type": "string"},
                "expected_value": {"type": "number"},
                "actual_value": {"type": "number"},
                "tolerance": {"type": "number", "default": 0.0},
                "observed_metric_name": {"type": "string"},
            },
            ["metric_name", "expected_value", "actual_value"],
        ),
        handler=compare_claim_metric,
    ),
    "detect_seed_issue": ToolSpec(
        name="detect_seed_issue",
        description="Detect obvious randomness without seed control in a Python artifact.",
        input_schema=_schema(
            {"script_path": {"type": "string"}},
            ["script_path"],
        ),
        handler=detect_seed_issue,
    ),
    "detect_leakage": ToolSpec(
        name="detect_leakage",
        description="Detect simple CSV target leakage patterns.",
        input_schema=_schema(
            {
                "dataset_path": {"type": "string"},
                "target_column": {"type": "string"},
            },
            ["dataset_path", "target_column"],
        ),
        handler=detect_leakage,
    ),
    "scan_case_for_secrets": ToolSpec(
        name="scan_case_for_secrets",
        description="Scan case files for common secret-like values before execution.",
        input_schema=_schema(
            {"path": {"type": "string"}},
            ["path"],
        ),
        handler=scan_case_for_secrets,
    ),
    "export_case_report": ToolSpec(
        name="export_case_report",
        description="Run an audit and export Markdown and JSON report files.",
        input_schema=_schema(
            {
                "case_path": {"type": "string"},
                "output_dir": {"type": "string"},
            },
            ["case_path", "output_dir"],
        ),
        handler=export_case_report,
    ),
}

