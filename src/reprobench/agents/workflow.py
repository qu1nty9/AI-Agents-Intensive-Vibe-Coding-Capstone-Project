"""Foundation workflow for the ReproBench Agent.

The milestone-0 workflow is intentionally deterministic. It defines the contract
that later LLM-backed or ADK-backed agents will satisfy.
"""

from __future__ import annotations

from pathlib import Path

from reprobench.benchmark.cases import CaseSpecError, load_case_spec
from reprobench.models import (
    AuditFinding,
    CaseSpec,
    EvidenceReport,
    ExecutionResult,
    MetricComparison,
    ReproductionPlan,
    ToolCall,
    Verdict,
)
from reprobench.tools import (
    classify_execution_error,
    compare_metric,
    detect_data_leakage,
    detect_missing_seed,
    run_python_script,
    scan_for_secrets,
)


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
    """Run the local reproducibility audit workflow for a benchmark case."""

    try:
        spec = load_case_spec(case_path)
    except CaseSpecError as exc:
        plan = build_initial_plan(case_path)
        return EvidenceReport(
            case_name=plan.case_name,
            verdict=Verdict.BLOCKED,
            plan=plan,
            tool_calls=(ToolCall("load_case_spec", {"path": str(case_path)}, "failed"),),
            findings=(
                AuditFinding(
                    severity="error",
                    title="Case spec unavailable",
                    detail=str(exc),
                ),
            ),
            summary="Audit blocked because the benchmark case spec could not be loaded.",
        )

    plan = build_initial_plan(case_path)
    tool_calls: list[ToolCall] = [
        ToolCall("load_case_spec", {"path": str(case_path)}, "completed"),
        ToolCall("validate_case_path", {"path": str(case_path)}, "completed"),
    ]
    findings: list[AuditFinding] = [_spec_finding(case_path)]

    secret_findings = scan_for_secrets(spec.path)
    tool_calls.append(
        ToolCall(
            "scan_for_secrets",
            {"path": str(spec.path), "findings": len(secret_findings)},
            "completed",
        )
    )
    findings.extend(secret_findings)
    if secret_findings:
        return _build_report(
            spec=spec,
            plan=plan,
            verdict=Verdict.UNSAFE_TO_RUN,
            tool_calls=tool_calls,
            findings=findings,
            summary="Audit stopped because secret-like values were detected.",
        )

    if "detect_missing_seed" in spec.checks and spec.artifact_path is not None:
        seed_findings = detect_missing_seed(spec.artifact_path)
        tool_calls.append(
            ToolCall(
                "detect_missing_seed",
                {"path": str(spec.artifact_path), "findings": len(seed_findings)},
                "completed",
            )
        )
        findings.extend(seed_findings)

    if (
        "detect_data_leakage" in spec.checks
        and spec.dataset_path is not None
        and spec.target_column is not None
    ):
        leakage_findings = detect_data_leakage(spec.dataset_path, spec.target_column)
        tool_calls.append(
            ToolCall(
                "detect_data_leakage",
                {
                    "dataset_path": str(spec.dataset_path),
                    "target_column": spec.target_column,
                    "findings": len(leakage_findings),
                },
                "completed",
            )
        )
        findings.extend(leakage_findings)

    execution_results = _execute_case(spec, tool_calls)
    _classify_execution_errors(spec, execution_results, findings, tool_calls)
    comparison = _compare_first_metric(spec, execution_results, findings, tool_calls)
    verdict = _decide_verdict(execution_results, comparison, findings)
    summary = _summary_for_verdict(verdict)

    return EvidenceReport(
        case_name=plan.case_name,
        verdict=verdict,
        plan=plan,
        tool_calls=tuple(tool_calls),
        findings=tuple(findings),
        summary=summary,
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


def _execute_case(spec: CaseSpec, tool_calls: list[ToolCall]) -> tuple[ExecutionResult, ...]:
    if spec.artifact_path is None:
        return ()

    run_count = 3 if "run_repeated_trials" in spec.checks else 1
    results: list[ExecutionResult] = []
    for run_index in range(run_count):
        result = run_python_script(spec.artifact_path)
        status = "completed" if result.return_code == 0 and not result.timed_out else "failed"
        tool_name = "run_repeated_trials" if run_count > 1 else "run_python_script"
        tool_calls.append(
            ToolCall(
                tool_name,
                {
                    "path": str(spec.artifact_path),
                    "run_index": run_index + 1,
                    "return_code": result.return_code,
                    "timed_out": result.timed_out,
                },
                status,
            )
        )
        results.append(result)
    return tuple(results)


def _compare_first_metric(
    spec: CaseSpec,
    execution_results: tuple[ExecutionResult, ...],
    findings: list[AuditFinding],
    tool_calls: list[ToolCall],
) -> MetricComparison | None:
    if spec.claim is None:
        return None

    successful_outputs = [
        result.parsed_output
        for result in execution_results
        if result.return_code == 0 and result.parsed_output is not None
    ]
    if not successful_outputs:
        _add_execution_failure_findings(execution_results, findings)
        return None

    comparison = compare_metric(spec.claim, successful_outputs[0])
    status = "completed" if comparison.passed else "failed"
    tool_calls.append(
        ToolCall(
            "compare_metric",
            {
                "metric_name": comparison.metric_name,
                "expected": comparison.expected_value,
                "actual": comparison.actual_value,
                "tolerance": comparison.tolerance,
                "delta": comparison.delta,
            },
            status,
        )
    )
    if comparison.passed:
        findings.append(
            AuditFinding(
                severity="info",
                title="Metric reproduced within tolerance",
                detail=(
                    f"{comparison.metric_name}: expected {comparison.expected_value}, "
                    f"observed {comparison.actual_value}, tolerance {comparison.tolerance}."
                ),
            )
        )
    else:
        findings.append(
            AuditFinding(
                severity="error",
                title="Metric mismatch",
                detail=(
                    f"{comparison.metric_name}: expected {comparison.expected_value}, "
                    f"observed {comparison.actual_value}, tolerance {comparison.tolerance}."
                ),
            )
        )

    _add_instability_finding(successful_outputs, findings)
    return comparison


def _classify_execution_errors(
    spec: CaseSpec,
    execution_results: tuple[ExecutionResult, ...],
    findings: list[AuditFinding],
    tool_calls: list[ToolCall],
) -> None:
    if "classify_execution_error" not in spec.checks:
        return
    failed_results = [
        result for result in execution_results if result.return_code != 0 or result.timed_out
    ]
    if not failed_results:
        return

    classified: list[AuditFinding] = []
    for result in failed_results:
        classified.extend(classify_execution_error(result))
    tool_calls.append(
        ToolCall(
            "classify_execution_error",
            {"failures": len(failed_results), "findings": len(classified)},
            "completed",
        )
    )
    findings.extend(classified)


def _add_execution_failure_findings(
    execution_results: tuple[ExecutionResult, ...],
    findings: list[AuditFinding],
) -> None:
    if not execution_results:
        findings.append(
            AuditFinding(
                severity="error",
                title="No execution attempted",
                detail="The case does not define an executable artifact.",
            )
        )
        return

    for result in execution_results:
        if result.return_code != 0 or result.timed_out:
            reason = "execution timed out" if result.timed_out else "execution failed"
            stderr_tail = result.stderr.strip().splitlines()[-1:] or [""]
            findings.append(
                AuditFinding(
                    severity="error",
                    title="Execution blocked",
                    detail=f"{reason}; return_code={result.return_code}; stderr={stderr_tail[0]}",
                )
            )


def _add_instability_finding(successful_outputs: list[dict], findings: list[AuditFinding]) -> None:
    values = [
        output.get("value")
        for output in successful_outputs
        if output.get("metric_name") and output.get("value") is not None
    ]
    if len(set(values)) > 1:
        findings.append(
            AuditFinding(
                severity="warning",
                title="Metric instability across repeated runs",
                detail=f"Observed metric values: {values}",
            )
        )


def _decide_verdict(
    execution_results: tuple[ExecutionResult, ...],
    comparison: MetricComparison | None,
    findings: list[AuditFinding],
) -> Verdict:
    if any(finding.severity == "critical" for finding in findings):
        return Verdict.UNSAFE_TO_RUN

    if any(result.return_code != 0 or result.timed_out for result in execution_results):
        return Verdict.BLOCKED

    warning_titles = {finding.title for finding in findings if finding.severity == "warning"}
    if warning_titles:
        return Verdict.PARTIALLY_REPRODUCED

    if comparison is None:
        return Verdict.BLOCKED

    if not comparison.passed:
        return Verdict.NOT_REPRODUCED

    return Verdict.REPRODUCED


def _summary_for_verdict(verdict: Verdict) -> str:
    if verdict == Verdict.REPRODUCED:
        return "The claimed result reproduced within tolerance."
    if verdict == Verdict.PARTIALLY_REPRODUCED:
        return "The metric evidence is incomplete or compromised by audit findings."
    if verdict == Verdict.NOT_REPRODUCED:
        return "The observed metric contradicts the claim."
    if verdict == Verdict.UNSAFE_TO_RUN:
        return "Execution was stopped by safety checks."
    return "The audit was blocked before a reproducibility verdict could be reached."


def _build_report(
    spec: CaseSpec,
    plan: ReproductionPlan,
    verdict: Verdict,
    tool_calls: list[ToolCall],
    findings: list[AuditFinding],
    summary: str,
) -> EvidenceReport:
    return EvidenceReport(
        case_name=spec.name,
        verdict=verdict,
        plan=plan,
        tool_calls=tuple(tool_calls),
        findings=tuple(findings),
        summary=summary,
    )
