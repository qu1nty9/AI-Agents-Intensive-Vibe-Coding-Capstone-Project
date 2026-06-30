# Final Video Plan

Target length: 4:30-5:00.

Goal: show that ReproBench Agent is not just a concept. It is a reproducible agent workflow with benchmark evidence, MCP-facing tools, safety controls, generated reports, and a public dashboard.

## Core Story

The video should prove one idea:

> A reproduced metric is not the same thing as trustworthy evidence.

Use the `data_leakage` case as the main story. The experiment claims `accuracy = 1.0`; ReproBench reproduces the number, detects target leakage, and returns `partially_reproduced`. That is the strongest demonstration of the project.

## Screen Setup

Use three windows or tabs:

- Browser: public dashboard or local `reports/sample/dashboard/index.html`.
- Terminal: repository root.
- Editor/browser tab: `reports/sample/data_leakage/report.md`, `docs/evidence_matrix.md`, and optionally `docs/architecture.md`.

Keep the terminal font large enough for the commands and `5/5` result to be readable.

## Segment Plan

### 0:00-0:25 - Hook

On screen:

- Show the dashboard title and benchmark proof.

Say:

Machine learning results are easy to claim and harder to verify. A notebook can report a strong score, but that score might depend on a missing seed, a broken environment, a metric mismatch, or data leakage. ReproBench Agent turns ML claims into auditable evidence.

### 0:25-0:55 - Product

On screen:

- Dashboard hero.
- Benchmark proof `5/5`.
- Current demo verdict `partially_reproduced`.
- Evidence attachments.

Say:

The agent reads an experiment case, extracts the claimed metric, builds a reproduction plan, runs controlled tools, audits the evidence, and exports a report. The key point is that it produces artifacts: verdicts, findings, tool traces, JSON, Markdown, and this dashboard.

### 0:55-1:25 - Evidence Map

On screen:

- `docs/evidence_matrix.md` or the dashboard `Judging Evidence Matrix` section.

Say:

This matrix is the judging index. Each major project claim maps to a proof artifact and a command: the agent workflow, benchmark evaluation, MCP tools, safety controls, and the public dashboard generation.

What to do:

- Point to `Agent workflow -> make sample-report`.
- Point to `Evaluation -> make audit-cases`.
- Point to `MCP tools -> make mcp-demo`.
- Point to `Safety -> make test`.

### 1:25-2:05 - Benchmark Proof

On screen:

- Terminal at repository root.

Run:

```bash
make audit-cases
```

Say:

The benchmark suite has five controlled cases: clean baseline, metric mismatch, seed instability, missing dependency, and data leakage. The audit is measurable because every case has an expected verdict.

What to show:

- The line `Expected verdicts matched: 5/5`.
- At least two rows, including `data_leakage` and `metric_mismatch`.

### 2:05-3:15 - Main Demo: Data Leakage

On screen:

- Terminal.

Run:

```bash
make sample-report
make dashboard
```

Then open:

- `reports/sample/data_leakage/report.md`
- `reports/sample/dashboard/index.html` or the public dashboard

Say:

The data leakage case claims `accuracy = 1.0`. A naive checker would accept the result because the metric reproduces. ReproBench reproduces the metric, but also detects that `leaky_target_copy` exactly matches the target column. That changes the verdict to `partially_reproduced`.

What to show:

- Verdict: `partially_reproduced`.
- Tool trace: `detect_data_leakage`, `run_python_script`, `compare_metric`.
- Finding: `Potential target leakage`.
- Summary that the metric evidence is incomplete or compromised.

### 3:15-4:00 - MCP And Safety

On screen:

- Terminal.

Run:

```bash
make mcp-demo
```

Say:

The same audit behavior is exposed through MCP-facing tools, so the agent capabilities are inspectable instead of hidden inside a single script. The project also treats experiment artifacts as untrusted inputs.

What to show:

- MCP output verdict: `partially_reproduced`.
- Tool trace in the JSON output.

Mention:

- path traversal checks;
- secret scanning;
- redaction;
- execution timeouts;
- blocked and unsafe verdicts.

### 4:00-4:45 - Close

On screen:

- Dashboard evidence matrix.
- Benchmark proof `5/5`.

Say:

ReproBench Agent is built for reviewers, Kaggle users, and data scientists who need more than a confident answer. It gathers evidence, runs checks, preserves a tool trace, and makes the review reproducible. The final proof is the benchmark result: `5/5` expected verdicts matched, with a data leakage case where the metric reproduces but the evidence is not trustworthy.

## Commands To Use In The Video

Run only these commands on camera:

```bash
make audit-cases
make sample-report
make dashboard
make mcp-demo
```

Optional if there is enough time:

```bash
make ci
```

## What You Need To Do On The Video

1. Open the dashboard and show the `5/5` proof.
2. Show the judging evidence matrix.
3. Run `make audit-cases`.
4. Run `make sample-report`.
5. Open the data leakage report and point to the leakage finding.
6. Run `make dashboard` and show that the dashboard is generated from evidence artifacts.
7. Run `make mcp-demo`.
8. Close on the dashboard with the `partially_reproduced` verdict and `5/5` benchmark proof.

## What Not To Spend Time On

- Do not explain every file in the repository.
- Do not walk through every benchmark case in detail.
- Do not spend time installing dependencies.
- Do not show long code blocks unless you need to identify the agent workflow.
- Do not let terminal output dominate the video; use it only as proof.
