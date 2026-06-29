# ReproBench Agent: Evidence-First Reproducibility Audits for ML Experiments

**Subtitle:** An agent that turns machine learning claims into auditable reproduction reports.

## Problem

Machine learning projects often depend on notebooks, dependencies, random seeds, metrics, and data preparation details that are hard to verify quickly. A result can look strong while being fragile, incomplete, or misleading. This is especially familiar in Kaggle-style workflows: a notebook may report a high score, but a reviewer still needs to know whether the result reproduces, whether the metric matches the claim, whether the environment is complete, and whether there are warning signs such as data leakage.

ReproBench Agent focuses on that review problem. Instead of asking a model to simply say whether a result is trustworthy, it runs an evidence-first audit and produces artifacts that a human can inspect.

## Solution

ReproBench Agent reads a benchmark case, extracts the claimed result, builds a reproduction plan, runs controlled checks, audits the evidence, and exports a structured report. Each run produces a verdict:

- `reproduced`
- `partially_reproduced`
- `not_reproduced`
- `blocked`
- `unsafe_to_run`

The demo uses a compact benchmark suite with known expected verdicts. That makes the project measurable: the agent is not only generating plausible text, it is producing verdicts that can be checked against controlled outcomes.

## Why This Needs an Agent

Reproducibility review is a multi-step task. The system has to inspect case metadata, identify the claim, decide which checks matter, run tools, react to failures, compare observed metrics against expected values, detect audit warnings, and produce a final explanation. A single response is not enough; the value comes from coordinating tools and preserving a trace of what happened.

ReproBench uses a coordinator workflow with distinct responsibilities:

- case loading and validation;
- claim extraction from `case.json`;
- reproduction planning;
- security checks;
- controlled artifact execution;
- evidence auditing;
- report generation.

Every run exposes a tool trace. For example, the data leakage demo records `validate_path_policy`, `scan_for_secrets`, `detect_data_leakage`, `run_python_script`, and `compare_metric`.

## MCP and Tool Use

The project exposes core capabilities as MCP-facing tools:

- `inspect_case`
- `audit_case`
- `run_case_artifact`
- `compare_claim_metric`
- `detect_seed_issue`
- `detect_leakage`
- `scan_case_for_secrets`
- `validate_path_policy`
- `export_case_report`

There are two ways to exercise this layer. The dependency-free JSON-lines server and CLI commands make the tool contracts testable in any local environment. An optional FastMCP entrypoint is also included for environments with the MCP SDK installed.

## Security

ReproBench treats experiment artifacts as untrusted inputs. Implemented controls include:

- path policy checks that reject absolute paths and `../` traversal from `case.json`;
- secret scanning before execution;
- execution timeouts;
- redaction of stdout, stderr, and parsed JSON output;
- Python artifact execution without arbitrary shell commands from case specs.

If a secret-like value is detected, the verdict becomes `unsafe_to_run`. If execution fails due to environment problems, the verdict is `blocked` rather than incorrectly reported as `not_reproduced`.

## Evidence

The benchmark suite covers five scenarios:

| Case | Expected Verdict | Purpose |
| --- | --- | --- |
| `clean_baseline` | `reproduced` | Confirms the happy path. |
| `metric_mismatch` | `not_reproduced` | Rejects an overstated metric. |
| `seed_instability` | `partially_reproduced` | Flags missing seed control. |
| `missing_dependency` | `blocked` | Separates environment failure from disproven claims. |
| `data_leakage` | `partially_reproduced` | Shows that a metric can reproduce while evidence is compromised. |

Current benchmark result: **5/5 expected verdicts matched**.

The strongest demo case is `data_leakage`. The experiment reports `accuracy = 1.0`, so a naive metric check would accept the claim. ReproBench reproduces the number but also detects that `leaky_target_copy` exactly matches the target column. The final verdict is `partially_reproduced`, which is the important behavior: the agent distinguishes "the number reproduced" from "the evidence is trustworthy."

Generated evidence artifacts:

- `reports/sample/benchmark/benchmark_summary.md`
- `reports/sample/data_leakage/report.md`
- `reports/sample/dashboard/index.html`
- `docs/index.html` for GitHub Pages

## Demo Commands

```bash
make test
make audit-cases
make benchmark-report
make sample-report
make dashboard
make mcp-demo
```

The static dashboard summarizes benchmark coverage, the data leakage verdict, audit findings, and the tool trace in one page.

## Limitations and Future Work

The current benchmark is intentionally small and controlled. This makes the demo reproducible and easy to judge, but it is not yet a broad arbitrary-repository auditor. Future work should add notebook execution, containerized sandboxing, richer leakage heuristics, and LLM-backed claim extraction from Kaggle notebooks, papers, or README files.

The current project prioritizes the core principle: an agent should not merely answer whether a claim is believable. It should gather evidence, run checks, preserve the trace, and make the review reproducible.

