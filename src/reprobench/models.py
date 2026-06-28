"""Core domain models for reproducibility audits."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class Verdict(StrEnum):
    """Supported final verdicts for an experiment audit."""

    REPRODUCED = "reproduced"
    PARTIALLY_REPRODUCED = "partially_reproduced"
    NOT_REPRODUCED = "not_reproduced"
    BLOCKED = "blocked"
    UNSAFE_TO_RUN = "unsafe_to_run"


@dataclass(frozen=True)
class Claim:
    """A claimed experiment result extracted from a case or notebook."""

    metric_name: str
    expected_value: float | None = None
    tolerance: float | None = None
    source: str = "case_spec"


@dataclass(frozen=True)
class CaseSpec:
    """A reproducibility case submitted to the agent."""

    path: Path
    name: str
    title: str = ""
    description: str = ""
    artifact_path: Path | None = None
    claim: Claim | None = None
    expected_verdict: Verdict | None = None
    failure_mode: str = ""
    tags: tuple[str, ...] = ()
    checks: tuple[str, ...] = ()
    dataset_path: Path | None = None
    target_column: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class CaseValidationResult:
    """Validation outcome for a benchmark case directory."""

    case_path: Path
    valid: bool
    errors: tuple[str, ...] = ()
    spec: CaseSpec | None = None


@dataclass(frozen=True)
class ReproductionPlan:
    """A high-level plan the agent intends to execute."""

    case_name: str
    steps: tuple[str, ...]
    safety_checks: tuple[str, ...] = ()


@dataclass(frozen=True)
class ToolCall:
    """A visible tool invocation captured in the trace."""

    name: str
    inputs: dict[str, Any] = field(default_factory=dict)
    status: str = "planned"


@dataclass(frozen=True)
class AuditFinding:
    """A finding produced by the evidence auditor."""

    severity: str
    title: str
    detail: str


@dataclass(frozen=True)
class EvidenceReport:
    """Final report returned by the workflow."""

    case_name: str
    verdict: Verdict
    plan: ReproductionPlan
    tool_calls: tuple[ToolCall, ...] = ()
    findings: tuple[AuditFinding, ...] = ()
    summary: str = ""
