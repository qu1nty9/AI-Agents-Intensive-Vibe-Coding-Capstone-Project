"""Evidence report export utilities."""

from __future__ import annotations

import json
from pathlib import Path

from reprobench.models import EvidenceReport


def report_to_dict(report: EvidenceReport) -> dict:
    """Serialize an evidence report to a JSON-compatible dictionary."""

    return {
        "case_name": report.case_name,
        "verdict": report.verdict.value,
        "summary": report.summary,
        "plan": {
            "steps": list(report.plan.steps),
            "safety_checks": list(report.plan.safety_checks),
        },
        "tool_calls": [
            {
                "name": tool_call.name,
                "inputs": tool_call.inputs,
                "status": tool_call.status,
            }
            for tool_call in report.tool_calls
        ],
        "findings": [
            {
                "severity": finding.severity,
                "title": finding.title,
                "detail": finding.detail,
            }
            for finding in report.findings
        ],
    }


def report_to_markdown(report: EvidenceReport) -> str:
    """Render an evidence report as Markdown."""

    lines = [
        f"# ReproBench Evidence Report: {report.case_name}",
        "",
        f"**Verdict:** `{report.verdict.value}`",
        "",
        f"**Summary:** {report.summary}",
        "",
        "## Reproduction Plan",
        "",
    ]
    for index, step in enumerate(report.plan.steps, start=1):
        lines.append(f"{index}. {step}")

    lines.extend(["", "## Safety Checks", ""])
    for check in report.plan.safety_checks:
        lines.append(f"- `{check}`")

    lines.extend(["", "## Tool Trace", ""])
    for index, tool_call in enumerate(report.tool_calls, start=1):
        lines.append(f"{index}. `{tool_call.name}` - **{tool_call.status}**")
        if tool_call.inputs:
            lines.append("")
            lines.append("   ```json")
            lines.append(f"   {json.dumps(tool_call.inputs, sort_keys=True)}")
            lines.append("   ```")

    lines.extend(["", "## Findings", ""])
    for finding in report.findings:
        lines.append(f"- **[{finding.severity}] {finding.title}:** {finding.detail}")

    lines.append("")
    return "\n".join(lines)


def write_report_bundle(report: EvidenceReport, output_dir: Path) -> tuple[Path, Path]:
    """Write Markdown and JSON report files into an output directory."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    markdown_path = destination / "report.md"
    json_path = destination / "report.json"
    markdown_path.write_text(report_to_markdown(report), encoding="utf-8")
    json_path.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    return markdown_path, json_path


def benchmark_summary_to_dict(rows: list[dict]) -> dict:
    """Serialize benchmark audit rows into a summary payload."""

    total = len(rows)
    matched = sum(1 for row in rows if row["matched"])
    return {
        "total_cases": total,
        "matched_cases": matched,
        "match_rate": matched / total if total else 0.0,
        "cases": rows,
    }


def benchmark_summary_to_markdown(rows: list[dict]) -> str:
    """Render benchmark audit rows as a Markdown summary."""

    payload = benchmark_summary_to_dict(rows)
    lines = [
        "# ReproBench Benchmark Summary",
        "",
        f"**Expected verdicts matched:** {payload['matched_cases']}/{payload['total_cases']}",
        "",
        "| Case | Expected | Actual | Status |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        status = "ok" if row["matched"] else "mismatch"
        lines.append(
            f"| `{row['name']}` | `{row['expected_verdict']}` | "
            f"`{row['actual_verdict']}` | {status} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_benchmark_summary(rows: list[dict], output_dir: Path) -> tuple[Path, Path]:
    """Write Markdown and JSON benchmark summary files."""

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    markdown_path = destination / "benchmark_summary.md"
    json_path = destination / "benchmark_summary.json"
    markdown_path.write_text(benchmark_summary_to_markdown(rows), encoding="utf-8")
    json_path.write_text(
        json.dumps(benchmark_summary_to_dict(rows), indent=2),
        encoding="utf-8",
    )
    return markdown_path, json_path
