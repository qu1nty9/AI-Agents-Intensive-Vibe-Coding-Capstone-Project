# Demo Script

Target video length: under 5 minutes.

## 0:00-0:30 - Problem

Machine learning notebooks often make claims that are hard to verify. A score may depend on a hidden seed, a fragile environment, a metric mismatch, or even data leakage.

## 0:30-1:00 - Solution

ReproBench Agent checks ML experiment reproducibility by reading the case, planning checks, running tools, auditing evidence, and exporting a report.

## 1:00-1:40 - Architecture

Show the architecture diagram:

- Coordinator;
- Claim Extractor;
- Planner;
- Security Guard;
- Executor;
- MCP tools;
- Evidence Auditor;
- Reporter.

## 1:40-3:30 - Live Demo

Recommended final demo case: `data_leakage`.

Show:

```bash
make benchmark-report
make sample-report
make dashboard
```

Then open the generated report and point out:

- extracted claim;
- plan;
- tool trace;
- observed metric;
- leakage finding;
- final verdict;
- recommended fix.
- the dashboard view.

Also show the full benchmark proof:

```bash
make audit-cases
```

Show the MCP-facing tool wrapper:

```bash
make mcp-tools
make mcp-demo
```

## 3:30-4:20 - Evidence and Safety

Show sample reports and tests. Mention that untrusted code is treated carefully through path policy checks, secret scanning, timeouts, and redaction.

```bash
reprobench mcp call validate_path_policy --args-json '{"case_path":"examples/cases/data_leakage"}'
```

Open:

- `reports/sample/benchmark/benchmark_summary.md`
- `reports/sample/data_leakage/report.md`
- `reports/sample/dashboard/index.html`

## 4:20-5:00 - Close

State why this matters for Kaggle and ML work:

> ReproBench Agent does not just answer whether a result is believable. It gathers evidence and makes the review reproducible.
