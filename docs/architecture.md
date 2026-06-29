# ReproBench Agent Architecture

## System Goal

ReproBench Agent checks whether an ML experiment claim is reproducible and exports an evidence report that a human reviewer can audit.

The system should be judged by artifacts, not by conversational polish:

- extracted claim;
- reproduction plan;
- tool-call trace;
- execution evidence;
- audit findings;
- final verdict.

## Target Workflow

```text
User / Demo Case
      |
      v
Benchmark Case Loader
      |
      v
Coordinator Agent
      |
      +--> Claim Extractor
      |
      +--> Reproduction Planner
      |
      +--> Security Guard
      |
      +--> Execution Agent
      |        |
      |        v
      |    MCP Tools
      |
      +--> Evidence Auditor
      |
      v
Report Generator
```

## Agent Responsibilities

### Benchmark Case Loader

Loads `case.json`, validates required fields, resolves artifact paths, and gives the agent an explicit expected verdict for benchmark evaluation.

### Coordinator Agent

Owns the run state and decides the next action. It should keep the workflow visible by emitting a structured trace.

### Claim Extractor

Identifies the experiment claim:

- metric name;
- expected value;
- tolerance;
- dataset assumptions;
- target column;
- execution entrypoint.

### Reproduction Planner

Creates the protocol the tools should execute. A plan should be specific enough that a human can inspect whether the agent chose reasonable checks.

### Security Guard

Prevents unsafe execution by scanning inputs, enforcing path boundaries, applying timeouts, and redacting secrets.

### Execution Agent

Invokes script and dataset tools. It does not silently execute arbitrary commands.

Current local tools:

- secret scanning;
- Python script execution with timeout;
- JSON metric parsing;
- metric comparison;
- missing seed detection;
- CSV leakage detection;
- execution error classification.

### Evidence Auditor

Compares outputs against claims and looks for common reproducibility failures:

- missing seed;
- metric mismatch;
- dependency failure;
- inconsistent split;
- possible data leakage;
- incomplete artifacts.

### Report Generator

Exports markdown and JSON reports with verdict, trace, findings, and recommended fixes.

## MCP Tools

Implemented MCP-facing tools:

- `inspect_case(case_path)`
- `audit_case(case_path)`
- `run_case_artifact(script_path, timeout_seconds)`
- `compare_claim_metric(metric_name, expected_value, actual_value, tolerance)`
- `detect_seed_issue(script_path)`
- `detect_leakage(dataset_path, target_column)`
- `scan_case_for_secrets(path)`
- `export_case_report(case_path, output_dir)`

## Verdicts

- `reproduced`: the claim was reproduced within tolerance.
- `partially_reproduced`: evidence supports part of the claim, but important caveats remain.
- `not_reproduced`: the observed evidence contradicts the claim.
- `blocked`: the run could not complete for a non-safety reason.
- `unsafe_to_run`: the input violated safety policy.

## Design Principle

The agent should never hide uncertainty. If a run is blocked, unsafe, or inconclusive, the report should say why and show the supporting evidence.
