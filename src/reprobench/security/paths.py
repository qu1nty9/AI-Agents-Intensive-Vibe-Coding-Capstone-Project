"""Path security policy for benchmark cases."""

from __future__ import annotations

from pathlib import Path

from reprobench.models import AuditFinding, CaseSpec


def resolve_child_path(base_dir: Path, child_path: str) -> Path:
    """Resolve a child path and reject absolute paths or directory traversal."""

    raw_child = Path(child_path)
    if raw_child.is_absolute():
        raise ValueError(f"path must be relative: {child_path}")

    base = Path(base_dir).resolve()
    resolved = (base / raw_child).resolve()
    if not is_relative_to(resolved, base):
        raise ValueError(f"path escapes case directory: {child_path}")
    return resolved


def is_relative_to(path: Path, root: Path) -> bool:
    """Return whether path is inside root after resolving both."""

    try:
        Path(path).resolve().relative_to(Path(root).resolve())
    except ValueError:
        return False
    return True


def display_path(path: Path, root: Path | None = None) -> str:
    """Return a stable display path, relative to root when possible."""

    base = Path.cwd() if root is None else Path(root)
    try:
        return str(Path(path).resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path)


def validate_case_path_policy(spec: CaseSpec) -> tuple[AuditFinding, ...]:
    """Validate that case artifacts stay inside the case directory."""

    findings: list[AuditFinding] = []
    if spec.artifact_path and not is_relative_to(spec.artifact_path, spec.path):
        findings.append(
            AuditFinding(
                severity="critical",
                title="Artifact path escapes case directory",
                detail=f"Artifact path is outside case directory: {spec.artifact_path}",
            )
        )
    if spec.dataset_path and not is_relative_to(spec.dataset_path, spec.path):
        findings.append(
            AuditFinding(
                severity="critical",
                title="Dataset path escapes case directory",
                detail=f"Dataset path is outside case directory: {spec.dataset_path}",
            )
        )
    return tuple(findings)
