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

Planned MCP tools:

- `inspect_notebook(path)`
- `extract_notebook_metadata(path)`
- `run_notebook(path, timeout_seconds)`
- `run_python_script(path, timeout_seconds)`
- `compare_metric(expected, actual, tolerance)`
- `detect_missing_seed(path)`
- `detect_data_leakage(dataset_path, target_column)`
- `scan_for_secrets(path)`
- `export_report(run_id, format)`
- `save_trace(run_id)`

## Verdicts

- `reproduced`: the claim was reproduced within tolerance.
- `partially_reproduced`: evidence supports part of the claim, but important caveats remain.
- `not_reproduced`: the observed evidence contradicts the claim.
- `blocked`: the run could not complete for a non-safety reason.
- `unsafe_to_run`: the input violated safety policy.

## Design Principle

The agent should never hide uncertainty. If a run is blocked, unsafe, or inconclusive, the report should say why and show the supporting evidence.
