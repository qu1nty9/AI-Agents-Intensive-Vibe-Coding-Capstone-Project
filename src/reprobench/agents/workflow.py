"""Foundation workflow for the ReproBench Agent.

The milestone-0 workflow is intentionally deterministic. It defines the contract
that later LLM-backed or ADK-backed agents will satisfy.
"""

from __future__ import annotations

from pathlib import Path

from reprobench.models import AuditFinding, EvidenceReport, ReproductionPlan, ToolCall, Verdict


def build_initial_plan(case_path: Path) -> ReproductionPlan:
    """Build the first visible reproduction plan for a case path."""

    case_name = _case_name(case_path)
    return ReproductionPlan(
        case_name=case_name,
        steps=(
            "Inspect case metadata and available experiment artifacts.",
            "Extract the claimed metric, expected value, and tolerance.",
            "Run safety checks before executing untrusted code.",
            "Execute the experiment in a controlled environment.",
            "Compare observed evidence against the claim.",
            "Export a reproducibility report with trace and findings.",
        ),
        safety_checks=(
            "scan_for_secrets",
            "validate_case_path",
            "enforce_execution_timeout",
        ),
    )


def run_foundation_workflow(case_path: Path) -> EvidenceReport:
    """Run a deterministic placeholder audit used to validate the repo foundation."""

    plan = build_initial_plan(case_path)
    tool_calls = (
        ToolCall("validate_case_path", {"path": str(case_path)}, "completed"),
        ToolCall("scan_for_secrets", {"path": str(case_path)}, "planned"),
        ToolCall("inspect_notebook", {"path": str(case_path)}, "planned"),
        ToolCall("export_report", {"case": plan.case_name}, "planned"),
    )
    findings = (
        AuditFinding(
            severity="info",
            title="Foundation workflow",
            detail="Core package and CLI are wired; benchmark execution arrives in the next milestone.",
        ),
    )
    return EvidenceReport(
        case_name=plan.case_name,
        verdict=Verdict.BLOCKED,
        plan=plan,
        tool_calls=tool_calls,
        findings=findings,
        summary="Milestone-0 dry run completed. No experiment execution was attempted yet.",
    )


def _case_name(case_path: Path) -> str:
    normalized = Path(case_path)
    return normalized.name or str(normalized)

