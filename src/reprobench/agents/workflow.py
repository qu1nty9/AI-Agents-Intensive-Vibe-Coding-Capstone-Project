"""Foundation workflow for the ReproBench Agent.

The milestone-0 workflow is intentionally deterministic. It defines the contract
that later LLM-backed or ADK-backed agents will satisfy.
"""

from __future__ import annotations

from pathlib import Path

from reprobench.benchmark.cases import CaseSpecError, load_case_spec
from reprobench.models import AuditFinding, EvidenceReport, ReproductionPlan, ToolCall, Verdict


def build_initial_plan(case_path: Path) -> ReproductionPlan:
    """Build the first visible reproduction plan for a case path."""

    case_name, checks = _case_context(case_path)
    safety_checks = _dedupe(
        (
            "scan_for_secrets",
            "validate_case_path",
            "enforce_execution_timeout",
            *checks,
        )
    )
    return ReproductionPlan(
        case_name=case_name,
        steps=(
            "Load and validate benchmark case metadata.",
            "Inspect case metadata and available experiment artifacts.",
            "Extract the claimed metric, expected value, and tolerance.",
            "Run safety checks before executing untrusted code.",
            "Execute the experiment in a controlled environment.",
            "Compare observed evidence against the claim.",
            "Export a reproducibility report with trace and findings.",
        ),
        safety_checks=safety_checks,
    )


def run_foundation_workflow(case_path: Path) -> EvidenceReport:
    """Run a deterministic placeholder audit used to validate the repo foundation."""

    plan = build_initial_plan(case_path)
    spec_finding = _spec_finding(case_path)
    tool_calls = (
        ToolCall("load_case_spec", {"path": str(case_path)}, "completed"),
        ToolCall("validate_case_path", {"path": str(case_path)}, "completed"),
        ToolCall("scan_for_secrets", {"path": str(case_path)}, "planned"),
        ToolCall("inspect_notebook", {"path": str(case_path)}, "planned"),
        ToolCall("export_report", {"case": plan.case_name}, "planned"),
    )
    findings = (
        spec_finding,
        AuditFinding(
            severity="info",
            title="Benchmark dry run",
            detail="Benchmark cases are loaded and validated; execution tools arrive in the next milestone.",
        ),
    )
    return EvidenceReport(
        case_name=plan.case_name,
        verdict=Verdict.BLOCKED,
        plan=plan,
        tool_calls=tool_calls,
        findings=findings,
        summary="Benchmark dry run completed. No experiment execution was attempted yet.",
    )


def _case_name(case_path: Path) -> str:
    normalized = Path(case_path)
    return normalized.name or str(normalized)


def _case_context(case_path: Path) -> tuple[str, tuple[str, ...]]:
    try:
        spec = load_case_spec(case_path)
    except CaseSpecError:
        return _case_name(case_path), ()
    return spec.name, spec.checks


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return tuple(result)


def _spec_finding(case_path: Path) -> AuditFinding:
    try:
        spec = load_case_spec(case_path)
    except CaseSpecError as exc:
        return AuditFinding(
            severity="warning",
            title="Case spec unavailable",
            detail=str(exc),
        )

    claim = spec.claim
    claim_detail = "no claim"
    if claim is not None:
        claim_detail = (
            f"{claim.metric_name}={claim.expected_value} "
            f"tolerance={claim.tolerance}"
        )
    return AuditFinding(
        severity="info",
        title=f"Loaded benchmark case: {spec.title}",
        detail=(
            f"Expected verdict is {spec.expected_verdict.value if spec.expected_verdict else 'unknown'}; "
            f"claim is {claim_detail}; failure mode is {spec.failure_mode or 'none'}."
        ),
    )
