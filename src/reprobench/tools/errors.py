"""Execution error classification tools."""

from __future__ import annotations

from reprobench.models import AuditFinding, ExecutionResult


def classify_execution_error(result: ExecutionResult) -> tuple[AuditFinding, ...]:
    """Classify common execution failures into reviewer-friendly findings."""

    if result.return_code == 0 and not result.timed_out:
        return ()

    stderr = result.stderr or ""
    if "ModuleNotFoundError" in stderr or "ImportError" in stderr:
        tail = stderr.strip().splitlines()[-1:] or ["dependency import failed"]
        return (
            AuditFinding(
                severity="error",
                title="Missing dependency",
                detail=tail[0],
            ),
        )

    if result.timed_out:
        return (
            AuditFinding(
                severity="error",
                title="Execution timeout",
                detail="The artifact exceeded the configured execution timeout.",
            ),
        )

    return (
        AuditFinding(
            severity="error",
            title="Execution failed",
            detail=f"The artifact exited with return_code={result.return_code}.",
        ),
    )

