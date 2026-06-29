# Final Video Script

Target duration: 4:30-5:00.

## 0:00-0:25 - Hook

Machine learning results are easy to claim and harder to verify. A notebook can report a strong score, but that score might depend on a missing seed, a broken environment, a metric mismatch, or even data leakage.

ReproBench Agent is an evidence-first agent for checking whether ML experiment claims are reproducible.

## 0:25-0:55 - Product

The agent reads an experiment case, extracts the claimed metric, builds a reproduction plan, runs controlled tools, audits the evidence, and exports a report.

The key idea is that the agent does not just answer with text. It produces artifacts: a verdict, a tool trace, findings, and reports that a reviewer can inspect.

## 0:55-1:25 - Architecture

Show `docs/architecture.md`.

The workflow has a case loader, coordinator, security guard, execution agent, evidence auditor, report generator, and MCP-facing tool registry.

Mention the main tools:

- `validate_path_policy`
- `scan_for_secrets`
- `detect_data_leakage`
- `run_python_script`
- `compare_metric`
- `export_case_report`

## 1:25-2:10 - Benchmark Proof

Run:

```bash
make audit-cases
```

Point out:

- five benchmark cases;
- five expected verdicts matched;
- the suite includes clean reproducibility, metric mismatch, seed instability, missing dependency, and data leakage.

Then run:

```bash
make benchmark-report
```

Open `reports/sample/benchmark/benchmark_summary.md`.

## 2:10-3:20 - Main Demo: Data Leakage

Run:

```bash
make sample-report
make dashboard
```

Open `reports/sample/dashboard/index.html`.

Explain:

- the demo case reports `accuracy = 1.0`;
- ReproBench reproduces the metric;
- the leakage tool finds that `leaky_target_copy` exactly matches the target column;
- final verdict is `partially_reproduced`;
- this is the distinction between reproducing a number and trusting the evidence.

Open `reports/sample/data_leakage/report.md` and show:

- reproduction plan;
- safety checks;
- tool trace;
- findings.

## 3:20-4:05 - MCP and Security

Run:

```bash
make mcp-demo
```

Explain that the same audit can be invoked through MCP-facing tools.

Then mention security controls:

- path traversal is blocked;
- secret-like values stop execution;
- stdout and stderr are redacted;
- scripts run with timeouts;
- environment failures become `blocked`, not `not_reproduced`.

## 4:05-4:45 - Close

ReproBench Agent turns ML claims into auditable evidence. It is built for reviewers, Kaggle users, and data scientists who need more than a confident answer. They need a reproducible audit trail.

Close with the dashboard and the benchmark result: `5/5` expected verdicts matched.

