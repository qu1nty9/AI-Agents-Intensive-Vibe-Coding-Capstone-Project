"""Benchmark case loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from reprobench.models import CaseSpec, CaseValidationResult, Claim, Verdict

CASE_SPEC_FILENAME = "case.json"


class CaseSpecError(ValueError):
    """Raised when a benchmark case spec is invalid."""


def list_case_dirs(root: Path = Path("examples/cases")) -> list[Path]:
    """Return case directories that contain a case spec."""

    if not root.exists():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / CASE_SPEC_FILENAME).exists())


def list_case_specs(root: Path = Path("examples/cases")) -> list[CaseSpec]:
    """Load all valid case specs under a root directory."""

    return [load_case_spec(path) for path in list_case_dirs(root)]


def load_case_spec(case_path: Path) -> CaseSpec:
    """Load and validate a benchmark case spec from a case directory."""

    case_dir = Path(case_path)
    spec_path = case_dir / CASE_SPEC_FILENAME
    if not spec_path.exists():
        raise CaseSpecError(f"missing {CASE_SPEC_FILENAME}: {case_dir}")

    try:
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CaseSpecError(f"invalid JSON in {spec_path}: {exc}") from exc

    errors = _validate_raw_spec(raw, case_dir)
    if errors:
        joined = "; ".join(errors)
        raise CaseSpecError(f"invalid case spec {spec_path}: {joined}")

    claim_raw = raw["claim"]
    artifact_path = case_dir / raw["artifact"]
    dataset_path = case_dir / raw["dataset"] if raw.get("dataset") else None

    return CaseSpec(
        path=case_dir,
        name=str(raw["name"]),
        title=str(raw.get("title", raw["name"])),
        description=str(raw.get("description", "")),
        artifact_path=artifact_path,
        claim=Claim(
            metric_name=str(claim_raw["metric_name"]),
            expected_value=float(claim_raw["expected_value"]),
            tolerance=float(claim_raw.get("tolerance", 0.0)),
            source=str(claim_raw.get("source", "case_spec")),
        ),
        expected_verdict=Verdict(str(raw["expected_verdict"])),
        failure_mode=str(raw.get("failure_mode", "")),
        tags=tuple(str(tag) for tag in raw.get("tags", [])),
        checks=tuple(str(check) for check in raw.get("checks", [])),
        dataset_path=dataset_path,
        target_column=raw.get("target_column"),
        notes=str(raw.get("notes", "")),
    )


def validate_case_directory(case_path: Path) -> CaseValidationResult:
    """Validate a case directory without raising on failure."""

    try:
        spec = load_case_spec(case_path)
    except CaseSpecError as exc:
        return CaseValidationResult(case_path=Path(case_path), valid=False, errors=(str(exc),))
    return CaseValidationResult(case_path=Path(case_path), valid=True, spec=spec)


def validate_all_cases(root: Path = Path("examples/cases")) -> list[CaseValidationResult]:
    """Validate all discovered cases under a root directory."""

    discovered = list_case_dirs(root)
    if not discovered:
        return [CaseValidationResult(case_path=root, valid=False, errors=("no case specs found",))]
    return [validate_case_directory(path) for path in discovered]


def _validate_raw_spec(raw: dict[str, Any], case_dir: Path) -> list[str]:
    errors: list[str] = []
    required_fields = ("schema_version", "name", "artifact", "claim", "expected_verdict")
    for field_name in required_fields:
        if field_name not in raw:
            errors.append(f"missing field: {field_name}")

    if raw.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    if "name" in raw and raw["name"] != case_dir.name:
        errors.append(f"name must match directory name: {case_dir.name}")

    artifact = raw.get("artifact")
    if artifact and not (case_dir / str(artifact)).exists():
        errors.append(f"artifact does not exist: {artifact}")

    dataset = raw.get("dataset")
    if dataset and not (case_dir / str(dataset)).exists():
        errors.append(f"dataset does not exist: {dataset}")

    claim = raw.get("claim")
    if not isinstance(claim, dict):
        errors.append("claim must be an object")
    else:
        for field_name in ("metric_name", "expected_value"):
            if field_name not in claim:
                errors.append(f"claim missing field: {field_name}")
        if "expected_value" in claim and not isinstance(claim["expected_value"], int | float):
            errors.append("claim.expected_value must be numeric")
        if "tolerance" in claim and not isinstance(claim["tolerance"], int | float):
            errors.append("claim.tolerance must be numeric")

    expected_verdict = raw.get("expected_verdict")
    if expected_verdict is not None:
        try:
            Verdict(str(expected_verdict))
        except ValueError:
            allowed = ", ".join(verdict.value for verdict in Verdict)
            errors.append(f"expected_verdict must be one of: {allowed}")

    for list_field in ("tags", "checks"):
        if list_field in raw and not isinstance(raw[list_field], list):
            errors.append(f"{list_field} must be a list")

    return errors
