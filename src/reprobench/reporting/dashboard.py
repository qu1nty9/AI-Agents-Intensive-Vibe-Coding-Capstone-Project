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
    match_rate = benchmark_summary.get(
        "match_rate",
        matched_cases / total_cases if total_cases else 0.0,
    )
    verdict = evidence_report.get("verdict", "unknown")
    summary = evidence_report.get("summary", "")

    case_rows = "\n".join(_case_row(case) for case in cases)
    tool_rows = "\n".join(_tool_row(index, tool) for index, tool in enumerate(tool_calls, start=1))
    finding_items = "\n".join(_finding_item(finding) for finding in findings)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ReproBench Agent Demo Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --background: #f8fafc;
      --foreground: #0f172a;
      --surface: #ffffff;
      --muted: #64748b;
      --muted-strong: #475569;
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --primary: #1e40af;
      --primary-soft: #dbeafe;
      --primary-muted: #eff6ff;
      --success: #047857;
      --success-soft: #d1fae5;
      --warning: #b45309;
      --warning-soft: #fef3c7;
      --danger: #b91c1c;
      --danger-soft: #fee2e2;
      --shadow: 0 24px 70px rgba(15, 23, 42, 0.10);
      --radius: 20px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ background: var(--background); }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        linear-gradient(180deg, #edf4ff 0, #f8fafc 360px),
        var(--background);
      color: var(--foreground);
      line-height: 1.5;
      overflow-x: hidden;
    }}
    a {{
      color: inherit;
      text-decoration: none;
    }}
    main {{
      width: min(1180px, calc(100vw - 32px));
      margin: 28px auto 48px;
      display: grid;
      gap: 18px;
      min-width: 0;
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{
      font-size: 34px;
      line-height: 1.1;
      margin-bottom: 12px;
      letter-spacing: 0;
    }}
    h2 {{ font-size: 18px; margin-bottom: 0; letter-spacing: 0; }}
    h3 {{ font-size: 15px; margin-bottom: 8px; letter-spacing: 0; }}
    p {{ color: var(--muted); }}
    .project-shell {{
      background: rgba(255, 255, 255, 0.94);
      border: 1px solid rgba(203, 213, 225, 0.9);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
      min-width: 0;
    }}
    .topbar {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 22px;
      border-bottom: 1px solid var(--border);
      background: rgba(248, 250, 252, 0.86);
    }}
    .breadcrumbs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      color: var(--muted);
      font-size: 13px;
      font-weight: 650;
      min-width: 0;
      max-width: 100%;
    }}
    .breadcrumb-current {{
      color: var(--foreground);
      overflow-wrap: anywhere;
    }}
    .actions {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      min-width: 0;
    }}
    .action {{
      min-height: 38px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--surface);
      color: var(--muted-strong);
      font-size: 13px;
      font-weight: 700;
      transition: border-color 180ms ease, background 180ms ease, color 180ms ease;
    }}
    .action:hover {{
      border-color: var(--primary);
      background: var(--primary-muted);
      color: var(--primary);
    }}
    .content {{
      padding: 30px;
      display: grid;
      gap: 28px;
      min-width: 0;
    }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(250px, 330px);
      gap: 24px;
      align-items: start;
      min-width: 0;
    }}
    .hero > * {{ min-width: 0; }}
    .title-row {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 6px;
    }}
    .eyebrow {{
      color: var(--primary);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .description {{
      max-width: 800px;
      margin-bottom: 0;
      color: var(--muted-strong);
      font-size: 16px;
      overflow-wrap: anywhere;
    }}
    .badge, .status, .severity {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 800;
      border: 1px solid transparent;
      white-space: nowrap;
    }}
    .badge-primary {{
      color: var(--primary);
      background: var(--primary-soft);
      border-color: #bfdbfe;
    }}
    .badge-success, .status-ok, .status-completed, .severity-info {{
      color: var(--success);
      background: var(--success-soft);
      border-color: #a7f3d0;
    }}
    .badge-warning, .status-warning, .severity-warning {{
      color: var(--warning);
      background: var(--warning-soft);
      border-color: #fde68a;
    }}
    .status-failed, .status-error, .severity-error, .severity-critical {{
      color: var(--danger);
      background: var(--danger-soft);
      border-color: #fecaca;
    }}
    .proof-panel {{
      border-left: 4px solid var(--primary);
      padding: 2px 0 2px 18px;
    }}
    .proof-label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .proof-value {{
      margin-top: 6px;
      font-size: 42px;
      line-height: 1;
      font-weight: 850;
      color: var(--foreground);
      font-variant-numeric: tabular-nums;
    }}
    .proof-subtext {{
      margin: 8px 0 0;
      color: var(--muted-strong);
      font-size: 14px;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: var(--surface);
      min-width: 0;
    }}
    .meta-item {{
      min-height: 100px;
      padding: 16px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
      border-right: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
      min-width: 0;
    }}
    .meta-item:nth-child(3n) {{ border-right: 0; }}
    .meta-item:nth-last-child(-n+3) {{ border-bottom: 0; }}
    .icon {{
      width: 34px;
      height: 34px;
      border-radius: 10px;
      display: inline-grid;
      place-items: center;
      color: var(--primary);
      background: var(--primary-muted);
      flex: 0 0 auto;
    }}
    .icon svg, .action svg, .attachment-icon svg {{
      width: 17px;
      height: 17px;
      stroke-width: 2;
    }}
    .meta-label {{
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .meta-value {{
      color: var(--foreground);
      font-size: 14px;
      font-weight: 750;
      overflow-wrap: anywhere;
    }}
    .tag-list, .assignees {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .avatar {{
      width: 30px;
      height: 30px;
      display: inline-grid;
      place-items: center;
      border-radius: 50%;
      color: #ffffff;
      background: var(--primary);
      font-size: 11px;
      font-weight: 850;
      box-shadow: 0 0 0 2px #ffffff;
    }}
    .section-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(300px, 0.75fr);
      gap: 22px;
      align-items: start;
      min-width: 0;
    }}
    .section-grid > * {{ min-width: 0; }}
    .section {{
      display: grid;
      gap: 14px;
      min-width: 0;
    }}
    .section-title {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}
    .attachments {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: var(--surface);
      min-width: 0;
    }}
    .attachment {{
      min-height: 112px;
      padding: 16px;
      border-right: 1px solid var(--border);
      transition: background 180ms ease, color 180ms ease;
      min-width: 0;
    }}
    .attachment:last-child {{ border-right: 0; }}
    .attachment:hover {{ background: var(--primary-muted); }}
    .attachment-icon {{
      width: 32px;
      height: 32px;
      display: inline-grid;
      place-items: center;
      border-radius: 10px;
      background: var(--primary-muted);
      color: var(--primary);
      margin-bottom: 12px;
    }}
    .attachment-name {{
      color: var(--foreground);
      font-size: 14px;
      font-weight: 800;
      overflow-wrap: anywhere;
    }}
    .attachment-meta {{
      margin-top: 2px;
      color: var(--muted);
      font-size: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    .table-wrap {{
      width: 100%;
      max-width: 100%;
      min-width: 0;
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: var(--surface);
    }}
    th, td {{
      border-bottom: 1px solid var(--border);
      padding: 13px 14px;
      text-align: left;
      vertical-align: top;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    th {{
      color: var(--muted);
      background: #f8fafc;
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
      white-space: nowrap;
    }}
    code {{
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 7px;
      padding: 3px 6px;
      font-size: 13px;
      color: #1e293b;
    }}
    ul {{ padding-left: 0; list-style: none; margin: 0; }}
    .finding-list {{
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: var(--surface);
    }}
    .finding-item {{
      padding: 15px;
      border-bottom: 1px solid var(--border);
    }}
    .finding-item:last-child {{ border-bottom: 0; }}
    .finding-title {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 6px;
    }}
    .finding-title strong {{ font-size: 14px; }}
    .finding-item p {{ margin: 0; font-size: 14px; }}
    .tool-index {{
      display: inline-grid;
      place-items: center;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: var(--primary-muted);
      color: var(--primary);
      font-size: 12px;
      font-weight: 850;
      font-variant-numeric: tabular-nums;
    }}
    .tool-name {{ font-weight: 800; }}
    .tool-input {{
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }}
    footer {{
      color: var(--muted);
      font-size: 13px;
      text-align: center;
      padding: 0 16px 28px;
    }}
    @media (max-width: 980px) {{
      .hero, .section-grid, .attachments {{ grid-template-columns: 1fr; }}
      .attachment {{ border-right: 0; border-bottom: 1px solid var(--border); }}
      .attachment:last-child {{ border-bottom: 0; }}
      .meta-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .meta-item:nth-child(3n) {{ border-right: 1px solid var(--border); }}
      .meta-item:nth-child(2n) {{ border-right: 0; }}
      .meta-item:nth-last-child(-n+3) {{ border-bottom: 1px solid var(--border); }}
      .meta-item:nth-last-child(-n+2) {{ border-bottom: 0; }}
    }}
    @media (max-width: 680px) {{
      main {{ width: calc(100vw - 20px); margin-top: 10px; }}
      .topbar, .content {{ padding: 16px; }}
      .topbar {{ align-items: flex-start; flex-direction: column; }}
      h1 {{ font-size: 28px; }}
      .description {{ font-size: 15px; }}
      .meta-grid {{ grid-template-columns: 1fr; }}
      .meta-item, .meta-item:nth-child(2n), .meta-item:nth-child(3n) {{
        border-right: 0;
        border-bottom: 1px solid var(--border);
      }}
      .meta-item:last-child {{ border-bottom: 0; }}
      .actions {{
        width: 100%;
        display: grid;
        grid-template-columns: 1fr;
      }}
      .action {{ width: 100%; justify-content: center; }}
      th, td {{ padding: 11px 12px; }}
    }}
    @media (max-width: 520px) {{
      main {{
        width: min(calc(100vw - 20px), 370px);
        margin: 10px 10px 48px;
      }}
      .breadcrumb-current {{
        max-width: 100%;
        flex-basis: 100%;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <article class="project-shell">
      <div class="topbar">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <span>Client Projects</span>
          <span aria-hidden="true">/</span>
          <span>Kaggle Freestyle</span>
          <span aria-hidden="true">/</span>
          <span class="breadcrumb-current">ReproBench Evidence Audit</span>
        </nav>
        <div class="actions">
          <a class="action" href="https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project" aria-label="Open GitHub repository">
            {_icon("github")}Repository
          </a>
          <a class="action" href="https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/" aria-label="Open public demo dashboard">
            {_icon("external")}Public demo
          </a>
        </div>
      </div>

      <div class="content">
        <section class="hero" aria-labelledby="dashboard-title">
          <div>
            <div class="title-row">
              <span class="eyebrow">AI Agents Intensive Capstone</span>
              <span class="badge badge-primary">Freestyle</span>
              <span class="badge badge-warning">{html.escape(str(verdict))}</span>
            </div>
            <h1 id="dashboard-title">ReproBench Agent Demo Dashboard</h1>
            <p class="description">Evidence-first reproducibility audit for ML experiment claims. This view packages the benchmark proof, the data leakage demo, and the tool trace into a judge-friendly project detail page.</p>
          </div>
          <aside class="proof-panel" aria-label="Benchmark proof summary">
            <div class="proof-label">Benchmark verdicts matched</div>
            <div class="proof-value">{matched_cases}/{total_cases}</div>
            <p class="proof-subtext">{float(match_rate):.0%} match rate across controlled reproduction cases.</p>
          </aside>
        </section>

        <section class="meta-grid" aria-label="Project metadata">
          <div class="meta-item">
            <span class="icon">{_icon("status")}</span>
            <div>
              <div class="meta-label">Status</div>
              <div class="meta-value"><span class="badge badge-success">Submission proof ready</span></div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("users")}</span>
            <div>
              <div class="meta-label">Agent roles</div>
              <div class="assignees">
                <span class="avatar" title="Coordinator">CO</span>
                <span class="avatar" title="Auditor">AU</span>
                <span class="avatar" title="Reporter">RP</span>
              </div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("calendar")}</span>
            <div>
              <div class="meta-label">Submission window</div>
              <div class="meta-value">June 28, 2026 -> July 6, 2026</div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("tag")}</span>
            <div>
              <div class="meta-label">Tags</div>
              <div class="tag-list">
                <span class="badge badge-primary">MCP tools</span>
                <span class="badge badge-primary">CI proof</span>
                <span class="badge badge-primary">Security</span>
              </div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("file")}</span>
            <div>
              <div class="meta-label">Demo case</div>
              <div class="meta-value">data_leakage audit with {len(tool_calls)} tool calls</div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("shield")}</span>
            <div>
              <div class="meta-label">Safety checks</div>
              <div class="meta-value">path policy, secret scan, timeout, redaction</div>
            </div>
          </div>
        </section>

        <section class="section" aria-labelledby="description-title">
          <div class="section-title">
            <h2 id="description-title">Project Brief</h2>
            <span class="badge badge-warning">{html.escape(str(verdict))}</span>
          </div>
          <p class="description">{html.escape(str(summary))}</p>
        </section>

        <section class="section" aria-labelledby="attachments-title">
          <div class="section-title">
            <h2 id="attachments-title">Evidence Attachments</h2>
            <span class="badge badge-success">Generated artifacts</span>
          </div>
          <div class="attachments">
            {_artifact_card("Benchmark summary", "5 controlled cases", "benchmark_summary.md")}
            {_artifact_card("Data leakage report", str(verdict), "report.md + report.json")}
            {_artifact_card("Static dashboard", "GitHub Pages ready", "docs/index.html")}
            {_artifact_card("MCP demo trace", f"{len(tool_calls)} tool calls", "audit_case")}
          </div>
        </section>

        <div class="section-grid">
          <section class="section" aria-labelledby="benchmark-title">
            <div class="section-title">
              <h2 id="benchmark-title">Benchmark Suite</h2>
              <span class="badge badge-success">{matched_cases}/{total_cases} matched</span>
            </div>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr><th>Case</th><th>Expected</th><th>Actual</th><th>Status</th></tr>
                </thead>
                <tbody>
                  {case_rows}
                </tbody>
              </table>
            </div>
          </section>

          <section class="section" aria-labelledby="findings-title">
            <div class="section-title">
              <h2 id="findings-title">Audit Findings</h2>
              <span class="badge badge-warning">{len(findings)} findings</span>
            </div>
            <ul class="finding-list">
              {finding_items}
            </ul>
          </section>
        </div>

        <section class="section" aria-labelledby="trace-title">
          <div class="section-title">
            <h2 id="trace-title">Task List / Tool Trace</h2>
            <span class="badge badge-primary">Agent workflow</span>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>No</th><th>Task</th><th>Category</th><th>Status</th><th>Evidence</th></tr>
              </thead>
              <tbody>
                {tool_rows}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </article>
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


def _tool_row(index: int, tool: dict[str, Any]) -> str:
    tool_name = str(tool.get("name", "unknown_tool"))
    status = str(tool.get("status", "unknown"))
    category = _tool_category(tool_name)
    evidence = _tool_evidence(tool.get("inputs", {}))
    return (
        "<tr>"
        f"<td><span class=\"tool-index\">{index}</span></td>"
        f"<td><span class=\"tool-name\">{html.escape(tool_name)}</span></td>"
        f"<td>{html.escape(category)}</td>"
        f"<td><span class=\"status status-{_status_class(status)}\">{html.escape(status)}</span></td>"
        f"<td><span class=\"tool-input\">{html.escape(evidence)}</span></td>"
        "</tr>"
    )


def _finding_item(finding: dict[str, Any]) -> str:
    severity = str(finding.get("severity", "info"))
    title = str(finding.get("title", "Audit finding"))
    detail = str(finding.get("detail", ""))
    return (
        "<li class=\"finding-item\">"
        "<div class=\"finding-title\">"
        f"<span class=\"severity severity-{_status_class(severity)}\">{html.escape(severity)}</span>"
        f"<strong>{html.escape(title)}</strong>"
        "</div>"
        f"<p>{html.escape(detail)}</p>"
        "</li>"
    )


def _artifact_card(name: str, meta: str, detail: str) -> str:
    return (
        "<div class=\"attachment\">"
        f"<span class=\"attachment-icon\">{_icon('paperclip')}</span>"
        f"<div class=\"attachment-name\">{html.escape(name)}</div>"
        f"<div class=\"attachment-meta\">{html.escape(meta)}</div>"
        f"<div class=\"attachment-meta\">{html.escape(detail)}</div>"
        "</div>"
    )


def _tool_category(tool_name: str) -> str:
    if "secret" in tool_name or "path" in tool_name:
        return "Safety"
    if "leakage" in tool_name or "metric" in tool_name:
        return "Audit"
    if "run" in tool_name or "script" in tool_name:
        return "Execution"
    if "load" in tool_name or "validate" in tool_name:
        return "Discovery"
    return "Workflow"


def _tool_evidence(inputs: Any) -> str:
    if not isinstance(inputs, dict) or not inputs:
        return "structured trace recorded"

    preferred_keys = ("path", "dataset_path", "metric_name", "return_code", "findings", "actual")
    parts = [f"{key}={inputs[key]}" for key in preferred_keys if key in inputs]
    if not parts:
        parts = [f"{key}={value}" for key, value in list(inputs.items())[:2]]
    return ", ".join(str(part) for part in parts)


def _icon(name: str) -> str:
    icons = {
        "calendar": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M8 2v4"/><path d="M16 2v4"/>'
            '<rect x="3" y="4" width="18" height="18" rx="2"/>'
            '<path d="M3 10h18"/></svg>'
        ),
        "external": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M15 3h6v6"/><path d="M10 14 21 3"/>'
            '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8'
            'a2 2 0 0 1 2-2h6"/></svg>'
        ),
        "file": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16'
            'a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
            '<path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/>'
            '<path d="M10 9H8"/></svg>'
        ),
        "github": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5'
            'c3 0 6-2 6-5.5a4.4 4.4 0 0 0-1.2-3.1'
            'a4.1 4.1 0 0 0-.1-3.1s-1-.3-3.3 1.2'
            'a11.5 11.5 0 0 0-6 0C7.1 2.5 6.1 2.8 6.1 2.8'
            'A4.1 4.1 0 0 0 6 5.9 4.4 4.4 0 0 0 4.8 9'
            'c0 3.5 3 5.5 6 5.5a4.8 4.8 0 0 0-1 3.5v4"/>'
            '<path d="M9 18c-4.5 2-5-2-7-2"/></svg>'
        ),
        "paperclip": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="m21.4 11.6-8.5 8.5a6 6 0 0 1-8.5-8.5'
            'l8.5-8.5a4 4 0 0 1 5.7 5.7l-8.5 8.5'
            'a2 2 0 1 1-2.8-2.8l7.8-7.8"/></svg>'
        ),
        "shield": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.7 8.9'
            'a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1'
            'c2 0 4.5-1.2 6.2-2.5a1.3 1.3 0 0 1 1.6 0'
            'C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/>'
            '<path d="m9 12 2 2 4-4"/></svg>'
        ),
        "status": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
        ),
        "tag": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M12.6 2H4a2 2 0 0 0-2 2v8.6'
            'a2 2 0 0 0 .6 1.4l7.4 7.4a2 2 0 0 0 2.8 0'
            'l8.6-8.6a2 2 0 0 0 0-2.8L14 2.6A2 2 0 0 0 12.6 2z"/>'
            '<path d="M7 7h.01"/></svg>'
        ),
        "users": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6'
            'a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
            '<path d="M22 21v-2a4 4 0 0 0-3-3.9"/>'
            '<path d="M16 3.1a4 4 0 0 1 0 7.8"/></svg>'
        ),
    }
    return icons.get(name, icons["file"])


def _status_class(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value.lower())
