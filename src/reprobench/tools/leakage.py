"""Simple data leakage checks for CSV benchmark datasets."""

from __future__ import annotations

import csv
from pathlib import Path

from reprobench.models import AuditFinding


def detect_data_leakage(dataset_path: Path, target_column: str) -> tuple[AuditFinding, ...]:
    """Detect columns that exactly copy the target value."""

    with Path(dataset_path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return ()

    columns = [column for column in rows[0] if column != target_column]
    findings: list[AuditFinding] = []
    for column in columns:
        values = [row.get(column) for row in rows]
        target_values = [row.get(target_column) for row in rows]
        if values == target_values:
            findings.append(
                AuditFinding(
                    severity="warning",
                    title="Potential target leakage",
                    detail=(
                        f"Column '{column}' exactly matches target column "
                        f"'{target_column}' for all {len(rows)} rows."
                    ),
                )
            )
        elif "target" in column.lower():
            findings.append(
                AuditFinding(
                    severity="warning",
                    title="Suspicious target-like feature",
                    detail=f"Column '{column}' contains 'target' in its name.",
                )
            )
    return tuple(findings)

