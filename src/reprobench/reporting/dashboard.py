"""Static dashboard generation for demo and submission artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def build_dashboard_html(benchmark_summary: dict[str, Any], evidence_report: dict[str, Any]) -> str:
    """Build a static HTML dashboard for ReproBench sample artifacts."""

    cases = benchmark_summary.get("cases", [])
    findings = evidence_report.get("findings", [])
    tool_calls = evidence_report.get("tool_calls", [])
    matched_cases = benchmark_summary.get("matched_cases", 0)
    total_cases = benchmark_summary.get("total_cases", len(cases))
    verdict = evidence_report.get("verdict", "unknown")

    case_rows = "\n".join(_case_row(case) for case in cases)

    tool_items = "\n".join(
        "<li>"
        f"<span class=\"tool-index\">{index}</span>"
        f"<span class=\"tool-name\">{html.escape(tool['name'])}</span>"
        f"<span class=\"status status-{_status_class(tool['status'])}\">{html.escape(tool['status'])}</span>"
        "</li>"
        for index, tool in enumerate(tool_calls, start=1)
    )

    finding_items = "\n".join(
        "<li>"
        f"<span class=\"severity severity-{_status_class(finding['severity'])}\">"
        f"{html.escape(finding['severity'])}</span>"
        f"<strong>{html.escape(finding['title'])}</strong>"
        f"<p>{html.escape(finding['detail'])}</p>"
        "</li>"
        for finding in findings
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ReproBench Agent Demo Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f8fb;
      --panel: #ffffff;
      --ink: #18202a;
      --muted: #657285;
      --line: #dce3ed;
      --accent: #2367d1;
      --ok: #166534;
      --warn: #9a5b00;
      --error: #b42318;
      --soft-ok: #e9f7ef;
      --soft-warn: #fff3d9;
      --soft-blue: #eaf1ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }}
    header {{
      background: var(--panel);
      border-bottom: 1px solid var(--line);
      padding: 28px min(5vw, 56px);
    }}
    main {{
      width: min(1180px, calc(100vw - 32px));
      margin: 24px auto 40px;
      display: grid;
      gap: 18px;
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; letter-spacing: 0; }}
    h2 {{ font-size: 18px; margin-bottom: 14px; letter-spacing: 0; }}
    h3 {{ font-size: 15px; margin-bottom: 8px; letter-spacing: 0; }}
    p {{ color: var(--muted); }}
    .subtitle {{ max-width: 850px; margin-bottom: 0; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}
    .metric, section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .metric-label {{ color: var(--muted); font-size: 13px; margin-bottom: 6px; }}
    .metric-value {{ font-size: 26px; font-weight: 700; }}
    .grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
      gap: 18px;
      align-items: start;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{ color: var(--muted); font-weight: 600; }}
    code {{
      background: #eef2f7;
      border: 1px solid #dfe6ef;
      border-radius: 5px;
      padding: 2px 5px;
      font-size: 13px;
    }}
    ul {{ padding-left: 0; list-style: none; margin: 0; }}
    li + li {{ margin-top: 10px; }}
    .tool-index {{
      display: inline-grid;
      place-items: center;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: var(--soft-blue);
      color: var(--accent);
      font-size: 12px;
      margin-right: 8px;
      font-weight: 700;
    }}
    .tool-name {{ font-weight: 650; margin-right: 8px; }}
    .status, .severity {{
      display: inline-block;
      border-radius: 999px;
      padding: 2px 8px;
      font-size: 12px;
      font-weight: 700;
    }}
    .status-ok, .status-completed, .severity-info {{
      color: var(--ok);
      background: var(--soft-ok);
    }}
    .status-failed, .severity-error, .severity-critical {{
      color: var(--error);
      background: #fdeceb;
    }}
    .severity-warning, .status-warning {{
      color: var(--warn);
      background: var(--soft-warn);
    }}
    .verdict {{
      display: inline-block;
      color: var(--warn);
      background: var(--soft-warn);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 13px;
      font-weight: 750;
      margin-bottom: 10px;
    }}
    .finding p {{ margin: 4px 0 0; }}
    footer {{
      color: var(--muted);
      font-size: 13px;
      padding: 0 min(5vw, 56px) 28px;
    }}
    @media (max-width: 800px) {{
      .metrics, .grid {{ grid-template-columns: 1fr; }}
      header {{ padding: 22px 16px; }}
      main {{ width: calc(100vw - 24px); }}
      th, td {{ padding: 9px 5px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>ReproBench Agent Demo Dashboard</h1>
    <p class="subtitle">Evidence-first reproducibility audit for ML experiment claims. The dashboard summarizes benchmark coverage and the strongest demo case: data leakage that reproduces numerically but should not be trusted.</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric">
        <div class="metric-label">Benchmark verdicts matched</div>
        <div class="metric-value">{matched_cases}/{total_cases}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Demo case verdict</div>
        <div class="metric-value">{html.escape(verdict)}</div>
      </div>
      <div class="metric">
        <div class="metric-label">Tool calls in demo trace</div>
        <div class="metric-value">{len(tool_calls)}</div>
      </div>
    </div>
    <div class="grid">
      <section>
        <h2>Benchmark Suite</h2>
        <table>
          <thead>
            <tr><th>Case</th><th>Expected</th><th>Actual</th><th>Status</th></tr>
          </thead>
          <tbody>
            {case_rows}
          </tbody>
        </table>
      </section>
      <section>
        <h2>Data Leakage Evidence</h2>
        <span class="verdict">{html.escape(verdict)}</span>
        <p>{html.escape(evidence_report.get('summary', ''))}</p>
        <h3>Findings</h3>
        <ul class="finding">
          {finding_items}
        </ul>
      </section>
    </div>
    <section>
      <h2>Tool Trace</h2>
      <ul>
        {tool_items}
      </ul>
    </section>
  </main>
  <footer>
    Generated from reports/sample/benchmark/benchmark_summary.json and reports/sample/data_leakage/report.json.
  </footer>
</body>
</html>
"""


def write_dashboard(
    benchmark_summary_path: Path,
    evidence_report_path: Path,
    output_path: Path,
) -> Path:
    """Read JSON report artifacts and write a static HTML dashboard."""

    benchmark_summary = json.loads(Path(benchmark_summary_path).read_text(encoding="utf-8"))
    evidence_report = json.loads(Path(evidence_report_path).read_text(encoding="utf-8"))
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        build_dashboard_html(benchmark_summary, evidence_report),
        encoding="utf-8",
    )
    return destination


def _code(value: Any) -> str:
    return f"<code>{html.escape(str(value))}</code>"


def _case_row(case: dict[str, Any]) -> str:
    status_text = "ok" if case["matched"] else "mismatch"
    status_class = "ok" if case["matched"] else "warning"
    return (
        "<tr>"
        f"<td>{_code(case['name'])}</td>"
        f"<td>{_code(case['expected_verdict'])}</td>"
        f"<td>{_code(case['actual_verdict'])}</td>"
        f"<td><span class=\"status status-{status_class}\">{status_text}</span></td>"
        "</tr>"
    )


def _status_class(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value.lower())
