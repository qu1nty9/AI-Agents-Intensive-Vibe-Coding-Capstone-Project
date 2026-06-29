"""Secret scanning tools for benchmark inputs."""

from __future__ import annotations

from pathlib import Path

from reprobench.models import AuditFinding
from reprobench.security.redaction import SECRET_PATTERNS

TEXT_SUFFIXES = {".py", ".json", ".md", ".txt", ".csv", ".yaml", ".yml"}


def scan_for_secrets(path: Path) -> tuple[AuditFinding, ...]:
    """Scan text files under a path for common secret patterns."""

    root = Path(path)
    files = [root] if root.is_file() else [item for item in root.rglob("*") if item.is_file()]
    findings: list[AuditFinding] = []
    for file_path in files:
        if file_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(
                    AuditFinding(
                        severity="critical",
                        title="Potential secret detected",
                        detail=f"Secret-like pattern found in {file_path}.",
                    )
                )
                break
    return tuple(findings)
