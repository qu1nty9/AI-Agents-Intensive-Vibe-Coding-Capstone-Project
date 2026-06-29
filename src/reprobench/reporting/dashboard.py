"""Static dashboard generation for demo and submission artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def build_dashboard_html(benchmark_summary: dict[str, Any], evidence_report: dict[str, Any]) -> str:
    """Build a static HTML dashboard for ReproBench sample artifacts."""

    cases = benchmark_summary.get("cases") or []
    findings = evidence_report.get("findings") or []
    tool_calls = evidence_report.get("tool_calls") or []
    matched_cases = benchmark_summary.get("matched_cases", 0)
    total_cases = benchmark_summary.get("total_cases", len(cases))
    match_rate = benchmark_summary.get(
        "match_rate",
        matched_cases / total_cases if total_cases else 0.0,
    )
    verdict = evidence_report.get("verdict", "unknown")
    summary = evidence_report.get("summary", "")
    match_rate_value = _safe_ratio(match_rate)
    match_rate_percent = round(match_rate_value * 100)
    progress_width = min(100, max(0, match_rate_percent))
    status_label, status_tone = _project_status(str(verdict))
    finding_summary = _finding_summary(findings)

    case_rows = "\n".join(_case_row(case) for case in cases) or _empty_row(
        4,
        "No benchmark cases were included in the summary artifact.",
    )
    tool_rows = "\n".join(
        _tool_row(index, tool) for index, tool in enumerate(tool_calls, start=1)
    ) or _empty_row(5, "No agent tool calls were recorded for this evidence report.")
    finding_items = "\n".join(_finding_item(finding) for finding in findings) or (
        "<li class=\"finding-item finding-empty\">No audit findings were reported.</li>"
    )
    evidence_rows = "\n".join(_evidence_row(row) for row in _judging_evidence_rows())
    style = _dashboard_style()

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ReproBench Agent Demo Dashboard</title>
  <style>
{style}
  </style>
</head>
<body>
  <a class="skip-link" href="#dashboard-content">Skip to dashboard content</a>
  <main class="workspace" id="dashboard-content">
    <article class="project-detail" aria-labelledby="dashboard-title">
      <header class="project-header">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <a href="https://www.kaggle.com/" aria-label="Open Kaggle">Kaggle</a>
          <span aria-hidden="true">/</span>
          <span>AI Agents Intensive</span>
          <span aria-hidden="true">/</span>
          <span aria-current="page">ReproBench Agent</span>
        </nav>
        <div class="header-actions" aria-label="Project links">
          <a class="icon-button" href="https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project" aria-label="Open GitHub repository">
            {_icon("github")}<span class="sr-only">Open GitHub repository</span>
          </a>
          <a class="icon-button" href="https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/" aria-label="Open public demo dashboard">
            {_icon("external")}<span class="sr-only">Open public demo dashboard</span>
          </a>
        </div>
      </header>

      <div class="content">
        <section class="hero" aria-labelledby="dashboard-title">
          <div class="hero-copy">
            <div class="title-row">
              <span class="eyebrow">Freestyle capstone</span>
              <span class="status-pill tone-{status_tone}">
                <span class="status-dot" aria-hidden="true"></span>
                {html.escape(status_label)}
              </span>
            </div>
            <h1 id="dashboard-title">ReproBench Evidence Project</h1>
            <p class="lede">A judge-facing project detail dashboard for an AI agent that turns ML experiment claims into reproducible, auditable evidence.</p>
            <div class="tag-list" aria-label="Project tags">
              <span class="badge tone-info">MCP tools</span>
              <span class="badge tone-success">CI proof</span>
              <span class="badge tone-warning">Leakage audit</span>
              <span class="badge tone-neutral">Static Pages demo</span>
            </div>
          </div>
          <aside class="score-panel" aria-label="Benchmark proof summary">
            <div class="score-label">Benchmark proof</div>
            <div class="score-value">{matched_cases}<span>/{total_cases}</span></div>
            <p>{match_rate_percent}% expected verdict match rate across controlled reproduction cases.</p>
            <div class="progress-track" aria-hidden="true">
              <span style="width: {progress_width}%"></span>
            </div>
          </aside>
        </section>

        <section class="meta-grid" aria-label="Project details">
          <div class="meta-item">
            <span class="icon">{_icon("status")}</span>
            <div>
              <div class="meta-label">Status</div>
              <div class="meta-value">Submission proof package ready</div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("users")}</span>
            <div>
              <div class="meta-label">Agent roles</div>
              <div class="assignees" aria-label="Coordinator, auditor, reporter">
                <span class="avatar" title="Coordinator">CO</span>
                <span class="avatar" title="Auditor">AU</span>
                <span class="avatar" title="Reporter">RP</span>
                <span class="assignee-copy">Coordinator, auditor, reporter</span>
              </div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("calendar")}</span>
            <div>
              <div class="meta-label">Deadline</div>
              <div class="meta-value">July 6, 2026 11:59 PM PT / July 7, 2026 09:59 MSK</div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("tag")}</span>
            <div>
              <div class="meta-label">Track</div>
              <div class="meta-value">Kaggle Freestyle</div>
            </div>
          </div>
          <div class="meta-item">
            <span class="icon">{_icon("file")}</span>
            <div>
              <div class="meta-label">Demo case</div>
              <div class="meta-value">data_leakage audit, {len(tool_calls)} recorded tool calls</div>
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

        <section class="brief-section" aria-labelledby="description-title">
          <div class="section-copy">
            <div class="section-title">
              <h2 id="description-title">Project Brief</h2>
              <span class="badge tone-{status_tone}">{html.escape(str(verdict))}</span>
            </div>
            <p class="description">ReproBench reads a case, creates a reproduction plan, runs safe local checks, audits the evidence, and exports a report that a reviewer can inspect. The live proof focuses on data leakage: the claimed metric reproduces, but trust is reduced because the audit detects target leakage.</p>
          </div>
          <aside class="verdict-panel" aria-label="Current demo verdict">
            <span class="eyebrow">Current demo verdict</span>
            <strong>{html.escape(str(verdict))}</strong>
            <p>{html.escape(str(summary))}</p>
          </aside>
        </section>

        <section class="section" aria-labelledby="attachments-title">
          <div class="section-title">
            <h2 id="attachments-title">Evidence Attachments</h2>
            <span class="badge tone-success">Generated artifacts</span>
          </div>
          <div class="attachments">
            {_artifact_card("Benchmark summary", "5 controlled cases", "benchmark_summary.md", "https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/blob/main/reports/sample/benchmark/benchmark_summary.md", "file")}
            {_artifact_card("Data leakage report", str(verdict), "report.md + report.json", "https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/blob/main/reports/sample/data_leakage/report.md", "shield")}
            {_artifact_card("Static dashboard", "GitHub Pages ready", "docs/index.html", "https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/", "external")}
            {_artifact_card("MCP demo trace", f"{len(tool_calls)} tool calls", "audit_case", "https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/blob/main/docs/mcp_server.md", "status")}
          </div>
        </section>

        <section class="section" aria-labelledby="matrix-title">
          <div class="section-title">
            <h2 id="matrix-title">Judging Evidence Matrix</h2>
            <span class="badge tone-info">Claim to proof</span>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>Rubric Lens</th><th>Proof Artifact</th><th>Verification</th><th>Status</th></tr>
              </thead>
              <tbody>
                {evidence_rows}
              </tbody>
            </table>
          </div>
        </section>

        <div class="section-grid">
          <section class="section" aria-labelledby="benchmark-title">
            <div class="section-title">
              <h2 id="benchmark-title">Benchmark Suite</h2>
              <span class="badge tone-success">{matched_cases}/{total_cases} matched</span>
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
              <span class="badge tone-warning">{html.escape(finding_summary)}</span>
            </div>
            <ul class="finding-list">
              {finding_items}
            </ul>
          </section>
        </div>

        <section class="section" aria-labelledby="trace-title">
          <div class="section-title">
            <h2 id="trace-title">Agent Task List</h2>
            <span class="badge tone-info">Tool trace</span>
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
    Generated from committed evidence artifacts: reports/sample/benchmark/benchmark_summary.json and reports/sample/data_leakage/report.json.
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


def _dashboard_style() -> str:
    return """
    :root {
      color-scheme: light;
      --background: #f6f7fb;
      --foreground: #111827;
      --surface: #ffffff;
      --surface-muted: #f8fafc;
      --muted: #64748b;
      --muted-strong: #475569;
      --border: #e2e8f0;
      --border-strong: #cbd5e1;
      --primary: #2557d6;
      --primary-soft: #e8efff;
      --success: #047857;
      --success-soft: #dff7ea;
      --warning: #b45309;
      --warning-soft: #fff4d6;
      --danger: #be123c;
      --danger-soft: #ffe4eb;
      --neutral-soft: #eef2f7;
      --radius: 8px;
      --shadow: 0 24px 60px rgba(15, 23, 42, 0.10);
    }

    * {
      box-sizing: border-box;
    }

    html {
      background: var(--background);
    }

    body {
      margin: 0;
      min-height: 100vh;
      background:
        linear-gradient(180deg, #eef3fb 0, #f6f7fb 320px),
        var(--background);
      color: var(--foreground);
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
        "Segoe UI", sans-serif;
      line-height: 1.5;
      overflow-x: hidden;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    a:focus-visible,
    button:focus-visible {
      outline: 3px solid rgba(37, 87, 214, 0.28);
      outline-offset: 3px;
    }

    h1,
    h2,
    h3,
    p {
      margin-top: 0;
    }

    h1 {
      margin-bottom: 14px;
      font-size: 36px;
      line-height: 1.08;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }

    h2 {
      margin-bottom: 0;
      font-size: 18px;
      line-height: 1.25;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }

    p {
      color: var(--muted-strong);
    }

    .skip-link {
      position: absolute;
      left: 16px;
      top: 12px;
      z-index: 10;
      transform: translateY(-140%);
      border-radius: var(--radius);
      background: var(--foreground);
      color: #ffffff;
      padding: 10px 14px;
      font-size: 14px;
      font-weight: 750;
      transition: transform 180ms ease;
    }

    .skip-link:focus {
      transform: translateY(0);
    }

    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    .workspace {
      width: min(1180px, calc(100vw - 32px));
      margin: 30px auto 48px;
      min-width: 0;
    }

    .project-detail {
      min-width: 0;
      max-width: 100%;
      overflow: hidden;
      border: 1px solid rgba(203, 213, 225, 0.95);
      border-radius: var(--radius);
      background: rgba(255, 255, 255, 0.96);
      box-shadow: var(--shadow);
    }

    .project-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      min-width: 0;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      background: rgba(248, 250, 252, 0.82);
    }

    .project-header > * {
      min-width: 0;
    }

    .breadcrumbs {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      min-width: 0;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }

    .breadcrumbs a {
      color: var(--primary);
    }

    .breadcrumbs [aria-current="page"] {
      color: var(--foreground);
      overflow-wrap: anywhere;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 0 0 auto;
    }

    .icon-button {
      width: 44px;
      height: 44px;
      display: inline-grid;
      place-items: center;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
      color: var(--muted-strong);
      transition:
        background 180ms ease,
        border-color 180ms ease,
        color 180ms ease,
        transform 180ms ease;
    }

    .icon-button:hover {
      border-color: rgba(37, 87, 214, 0.38);
      background: var(--primary-soft);
      color: var(--primary);
      transform: translateY(-1px);
    }

    .content {
      display: grid;
      gap: 28px;
      min-width: 0;
      padding: 30px;
    }

    .content > * {
      min-width: 0;
      max-width: 100%;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(290px, 360px);
      gap: 28px;
      align-items: start;
      min-width: 0;
    }

    .hero > * {
      min-width: 0;
    }

    .hero-copy {
      min-width: 0;
    }

    .title-row {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 10px;
    }

    .eyebrow {
      color: var(--primary);
      font-size: 12px;
      font-weight: 850;
      letter-spacing: 0;
      text-transform: uppercase;
    }

    .lede {
      max-width: 760px;
      margin-bottom: 18px;
      color: var(--muted-strong);
      font-size: 16px;
      overflow-wrap: anywhere;
    }

    .badge,
    .status,
    .severity,
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      width: fit-content;
      max-width: 100%;
      border: 1px solid transparent;
      border-radius: 999px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 800;
      line-height: 1.2;
      white-space: nowrap;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: currentColor;
      box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.9);
    }

    .tone-info {
      background: var(--primary-soft);
      border-color: #c9d8ff;
      color: var(--primary);
    }

    .tone-success,
    .status-ok,
    .status-matched,
    .status-complete,
    .status-completed,
    .severity-info {
      background: var(--success-soft);
      border-color: #b9edcf;
      color: var(--success);
    }

    .tone-warning,
    .status-warning,
    .status-partially-reproduced,
    .status-blocked,
    .severity-warning {
      background: var(--warning-soft);
      border-color: #f9dda0;
      color: var(--warning);
    }

    .tone-danger,
    .status-failed,
    .status-error,
    .status-not-reproduced,
    .severity-error,
    .severity-critical {
      background: var(--danger-soft);
      border-color: #fecdd8;
      color: var(--danger);
    }

    .tone-neutral,
    .status-unknown {
      background: var(--neutral-soft);
      border-color: var(--border);
      color: var(--muted-strong);
    }

    .tag-list,
    .assignees {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      min-width: 0;
    }

    .score-panel {
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background:
        linear-gradient(180deg, #ffffff 0, #f8fafc 100%);
      padding: 20px;
      min-width: 0;
      max-width: 100%;
    }

    .score-label {
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
    }

    .score-value {
      color: var(--foreground);
      font-size: 48px;
      line-height: 1;
      font-weight: 850;
      font-variant-numeric: tabular-nums;
    }

    .score-value span {
      color: var(--muted);
      font-size: 26px;
      font-weight: 750;
    }

    .score-panel p {
      margin: 10px 0 14px;
      font-size: 14px;
    }

    .progress-track {
      width: 100%;
      height: 9px;
      overflow: hidden;
      border-radius: 999px;
      background: #e5e7eb;
    }

    .progress-track span {
      display: block;
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, #0f766e, #2557d6);
    }

    .meta-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1px;
      min-width: 0;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--border);
    }

    .meta-item {
      min-width: 0;
      min-height: 104px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 16px;
      background: var(--surface);
    }

    .meta-item > div {
      min-width: 0;
      max-width: 100%;
    }

    .icon {
      width: 36px;
      height: 36px;
      display: inline-grid;
      place-items: center;
      flex: 0 0 auto;
      border-radius: var(--radius);
      background: var(--surface-muted);
      color: var(--primary);
    }

    .icon svg,
    .icon-button svg,
    .attachment-icon svg {
      width: 18px;
      height: 18px;
      stroke-width: 2;
    }

    .meta-label {
      margin-bottom: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
    }

    .meta-value {
      color: var(--foreground);
      font-size: 14px;
      font-weight: 750;
      overflow-wrap: anywhere;
    }

    .avatar {
      width: 30px;
      height: 30px;
      display: inline-grid;
      place-items: center;
      border-radius: 50%;
      background: var(--primary);
      color: #ffffff;
      font-size: 11px;
      font-weight: 850;
      box-shadow: 0 0 0 2px #ffffff;
    }

    .assignee-copy {
      color: var(--muted-strong);
      font-size: 13px;
      font-weight: 700;
      overflow-wrap: anywhere;
    }

    .brief-section {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(260px, 340px);
      gap: 18px;
      align-items: stretch;
      min-width: 0;
    }

    .section-copy,
    .verdict-panel {
      min-width: 0;
      max-width: 100%;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
      padding: 18px;
    }

    .verdict-panel {
      display: grid;
      gap: 8px;
      align-content: start;
      background: #fffdf7;
    }

    .verdict-panel strong {
      color: var(--foreground);
      font-size: 22px;
      line-height: 1.15;
      overflow-wrap: anywhere;
    }

    .verdict-panel p,
    .description {
      margin-bottom: 0;
      color: var(--muted-strong);
      overflow-wrap: anywhere;
    }

    .section {
      display: grid;
      gap: 14px;
      min-width: 0;
    }

    .section-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      min-width: 0;
    }

    .section-title > * {
      min-width: 0;
    }

    .attachments {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      min-width: 0;
    }

    .attachment {
      min-width: 0;
      max-width: 100%;
      min-height: 132px;
      display: grid;
      align-content: start;
      gap: 8px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
      padding: 16px;
      transition:
        border-color 180ms ease,
        background 180ms ease,
        transform 180ms ease;
    }

    .attachment:hover {
      border-color: rgba(37, 87, 214, 0.32);
      background: var(--surface-muted);
      transform: translateY(-1px);
    }

    .attachment-icon {
      width: 34px;
      height: 34px;
      display: inline-grid;
      place-items: center;
      border-radius: var(--radius);
      background: var(--primary-soft);
      color: var(--primary);
    }

    .attachment-name {
      color: var(--foreground);
      font-size: 14px;
      font-weight: 850;
      overflow-wrap: anywhere;
    }

    .attachment-meta {
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }

    .section-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.18fr) minmax(300px, 0.82fr);
      gap: 22px;
      align-items: start;
      min-width: 0;
    }

    .section-grid > * {
      min-width: 0;
    }

    .table-wrap {
      width: 100%;
      max-width: 100%;
      min-width: 0;
      overflow-x: auto;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    th,
    td {
      border-bottom: 1px solid var(--border);
      padding: 13px 14px;
      text-align: left;
      vertical-align: top;
    }

    tr:last-child td {
      border-bottom: 0;
    }

    th {
      background: var(--surface-muted);
      color: var(--muted);
      font-size: 12px;
      font-weight: 850;
      text-transform: uppercase;
      white-space: nowrap;
    }

    code {
      border: 1px solid var(--border);
      border-radius: 7px;
      background: #f1f5f9;
      color: #1e293b;
      padding: 3px 6px;
      font-size: 13px;
      overflow-wrap: anywhere;
    }

    ul {
      list-style: none;
      margin: 0;
      padding-left: 0;
    }

    .finding-list {
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
    }

    .finding-item {
      padding: 15px;
      border-bottom: 1px solid var(--border);
    }

    .finding-item:last-child {
      border-bottom: 0;
    }

    .finding-title {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 7px;
    }

    .finding-title strong {
      font-size: 14px;
      overflow-wrap: anywhere;
    }

    .finding-item p {
      margin: 0;
      color: var(--muted-strong);
      font-size: 14px;
      overflow-wrap: anywhere;
    }

    .finding-empty {
      color: var(--muted-strong);
      font-size: 14px;
    }

    .empty-cell {
      color: var(--muted-strong);
      font-size: 14px;
    }

    .tool-index {
      width: 28px;
      height: 28px;
      display: inline-grid;
      place-items: center;
      border-radius: 50%;
      background: var(--primary-soft);
      color: var(--primary);
      font-size: 12px;
      font-weight: 850;
      font-variant-numeric: tabular-nums;
    }

    .tool-name {
      font-weight: 850;
      overflow-wrap: anywhere;
    }

    .tool-input {
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }

    footer {
      color: var(--muted);
      font-size: 13px;
      text-align: center;
      padding: 0 16px 28px;
    }

    @media (max-width: 980px) {
      .hero,
      .brief-section,
      .section-grid {
        grid-template-columns: 1fr;
      }

      .attachments {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .meta-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 680px) {
      .workspace {
        width: calc(100vw - 20px);
        margin-top: 10px;
      }

      .project-header,
      .content {
        padding: 16px;
      }

      .project-header {
        align-items: flex-start;
        flex-direction: column;
      }

      .header-actions {
        width: 100%;
      }

      h1 {
        font-size: 29px;
      }

      .lede {
        font-size: 15px;
      }

      .meta-grid,
      .attachments {
        grid-template-columns: 1fr;
      }

      .section-title {
        align-items: flex-start;
        flex-direction: column;
      }

      .badge,
      .status-pill {
        white-space: normal;
      }

      th,
      td {
        padding: 11px 12px;
      }

      .table-wrap {
        overflow-x: visible;
      }

      table,
      thead,
      tbody,
      tr,
      th,
      td {
        display: block;
      }

      thead {
        position: absolute;
        width: 1px;
        height: 1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
      }

      tr {
        padding: 12px;
        border-bottom: 1px solid var(--border);
      }

      tr:last-child {
        border-bottom: 0;
      }

      td {
        display: grid;
        grid-template-columns: minmax(76px, 0.36fr) minmax(0, 1fr);
        gap: 10px;
        align-items: start;
        border-bottom: 0;
        padding: 7px 0;
      }

      td::before {
        content: attr(data-label);
        color: var(--muted);
        font-size: 11px;
        font-weight: 850;
        text-transform: uppercase;
      }

      td.empty-cell {
        display: block;
      }

      td.empty-cell::before {
        content: none;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
      }
    }
    """.strip()


def _safe_ratio(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _project_status(verdict: str) -> tuple[str, str]:
    normalized = verdict.lower()
    if normalized == "reproduced":
        return "Evidence reproduced", "success"
    if normalized == "partially_reproduced":
        return "Evidence issue surfaced", "warning"
    if normalized == "not_reproduced":
        return "Claim rejected", "danger"
    if normalized == "blocked":
        return "Execution blocked", "warning"
    return "Audit pending", "neutral"


def _finding_summary(findings: list[Any]) -> str:
    if not findings:
        return "0 findings"

    counts: dict[str, int] = {}
    for finding in findings:
        if isinstance(finding, dict):
            severity = str(finding.get("severity", "info")).lower()
        else:
            severity = "info"
        counts[severity] = counts.get(severity, 0) + 1

    ordered = ["critical", "error", "warning", "info"]
    parts = [f"{counts[key]} {key}" for key in ordered if counts.get(key)]
    extras = [f"{count} {key}" for key, count in sorted(counts.items()) if key not in ordered]
    return " / ".join(parts + extras)


def _empty_row(column_count: int, message: str) -> str:
    return (
        "<tr>"
        f"<td class=\"empty-cell\" colspan=\"{column_count}\">{html.escape(message)}</td>"
        "</tr>"
    )


def _code(value: Any) -> str:
    return f"<code>{html.escape(str(value))}</code>"


def _case_row(case: dict[str, Any]) -> str:
    matched = bool(case.get("matched"))
    status_text = "matched" if matched else "mismatch"
    status_class = "matched" if matched else "warning"
    return (
        "<tr>"
        f"<td data-label=\"Case\">{_code(case.get('name', 'unknown_case'))}</td>"
        f"<td data-label=\"Expected\">{_code(case.get('expected_verdict', 'unknown'))}</td>"
        f"<td data-label=\"Actual\">{_code(case.get('actual_verdict', 'unknown'))}</td>"
        f"<td data-label=\"Status\"><span class=\"status status-{status_class}\">"
        f"{status_text}</span></td>"
        "</tr>"
    )


def _judging_evidence_rows() -> list[dict[str, str]]:
    return [
        {
            "lens": "Agent workflow",
            "artifact": "workflow.py + data_leakage report",
            "verification": "make sample-report",
            "status": "complete",
        },
        {
            "lens": "Evaluation",
            "artifact": "5-case benchmark summary",
            "verification": "make audit-cases",
            "status": "complete",
        },
        {
            "lens": "MCP tools",
            "artifact": "MCP tool registry and audit_case trace",
            "verification": "make mcp-demo",
            "status": "complete",
        },
        {
            "lens": "Safety",
            "artifact": "path policy, secret scan, redaction tests",
            "verification": "make test",
            "status": "complete",
        },
        {
            "lens": "Public demo",
            "artifact": "GitHub Pages dashboard from evidence JSON",
            "verification": "make pages",
            "status": "complete",
        },
    ]


def _evidence_row(row: dict[str, str]) -> str:
    status = row.get("status", "unknown")
    return (
        "<tr>"
        f"<td data-label=\"Rubric Lens\"><span class=\"tool-name\">"
        f"{html.escape(row.get('lens', 'Evidence'))}</span></td>"
        f"<td data-label=\"Proof Artifact\">{html.escape(row.get('artifact', ''))}</td>"
        f"<td data-label=\"Verification\">{_code(row.get('verification', ''))}</td>"
        f"<td data-label=\"Status\"><span class=\"status status-{_status_class(status)}\">"
        f"{html.escape(status)}</span></td>"
        "</tr>"
    )


def _tool_row(index: int, tool: dict[str, Any]) -> str:
    tool_name = str(tool.get("name", "unknown_tool"))
    status = str(tool.get("status", "unknown"))
    category = _tool_category(tool_name)
    evidence = _tool_evidence(tool.get("inputs", {}))
    return (
        "<tr>"
        f"<td data-label=\"No\"><span class=\"tool-index\">{index}</span></td>"
        f"<td data-label=\"Task\"><span class=\"tool-name\">{html.escape(tool_name)}</span></td>"
        f"<td data-label=\"Category\">{html.escape(category)}</td>"
        f"<td data-label=\"Status\"><span class=\"status status-{_status_class(status)}\">"
        f"{html.escape(status)}</span></td>"
        f"<td data-label=\"Evidence\"><span class=\"tool-input\">{html.escape(evidence)}</span></td>"
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


def _artifact_card(name: str, meta: str, detail: str, href: str, icon: str) -> str:
    return (
        f"<a class=\"attachment\" href=\"{html.escape(href, quote=True)}\" "
        "target=\"_blank\" rel=\"noopener noreferrer\">"
        f"<span class=\"attachment-icon\">{_icon(icon)}</span>"
        f"<div class=\"attachment-name\">{html.escape(name)}</div>"
        f"<div class=\"attachment-meta\">{html.escape(meta)}</div>"
        f"<div class=\"attachment-meta\">{html.escape(detail)}</div>"
        "</a>"
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
