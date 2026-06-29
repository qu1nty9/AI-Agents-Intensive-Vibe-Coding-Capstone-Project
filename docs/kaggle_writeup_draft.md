# Kaggle Writeup Draft

## Title

ReproBench Agent: Evidence-First Reproducibility Audits for ML Experiments

## Subtitle

An agent that turns machine learning claims into auditable reproduction reports.

## Problem

Machine learning projects often depend on notebooks, dependencies, random seeds, metrics, and data preparation steps that are difficult to verify quickly. A result can look strong while being fragile, incomplete, or misleading.

For Kaggle users this problem is familiar: a notebook may report a strong score, but a reviewer still needs to know whether the result is reproducible, whether the metric matches the claim, whether the environment is complete, and whether there are signs of leakage.

## Solution

ReproBench Agent reads an experiment case, extracts the claimed result, plans a reproduction protocol, executes controlled checks through tools, audits the evidence, and exports a structured report.

The current demo focuses on a compact benchmark suite where each case has an expected verdict. This makes the project testable: the agent is not only producing plausible text, it is producing verdicts that can be checked against known outcomes.

## Why Agents

This task is agentic because it requires more than a single model response. The system must inspect artifacts, decide which checks matter, run tools, react to failures, compare evidence, and produce a transparent final verdict.

## Architecture

The system uses a coordinator workflow with specialized responsibilities:

- claim extraction;
- reproduction planning;
- security checks;
- controlled execution;
- evidence auditing;
- report generation.

Every run produces a visible tool trace. For example, the data leakage case records `validate_path_policy`, `scan_for_secrets`, `detect_data_leakage`, `run_python_script`, and `compare_metric`.

## MCP and Tools

The implementation exposes core capabilities as MCP-facing tools, including case inspection, audit execution, metric comparison, secret scanning, leakage checks, and report export.

The project includes a dependency-free JSON-lines smoke server for local testing and an optional FastMCP entrypoint for environments where the MCP SDK is installed.

## Security

The agent treats notebooks and experiment files as untrusted inputs. Implemented controls include secret scanning, path policy checks, execution timeouts, and redaction.

The path policy blocks absolute paths and directory traversal from `case.json`. Execution output is redacted before it is stored in reports. The current execution layer only runs Python artifacts directly and does not execute arbitrary shell commands from a case spec.

## Evidence

The project includes benchmark cases for clean reproducibility, missing dependencies, random seed instability, metric mismatch, and data leakage.

Current benchmark result: `5/5` expected verdicts matched.

The strongest demo is `data_leakage`: the metric reproduces at `accuracy = 1.0`, but the audit finds that `leaky_target_copy` exactly matches the target column. The final verdict is `partially_reproduced`, which is the key behavior: ReproBench distinguishes "the number can be reproduced" from "the evidence should be trusted."

Generated artifacts:

- `reports/sample/benchmark/benchmark_summary.md`
- `reports/sample/data_leakage/report.md`

## Limitations

The initial benchmark is intentionally small and controlled. The project prioritizes transparent evidence and reproducible demos over broad support for arbitrary repositories.

Future work should add notebook execution, containerized sandboxing, richer leakage heuristics, and LLM-backed claim extraction from arbitrary Kaggle notebooks or papers.
