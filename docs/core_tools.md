# Core Audit Tools

Milestone 2 adds deterministic local tools that let ReproBench produce real verdicts for the benchmark suite without external services.

## Tools

| Tool | Purpose |
| --- | --- |
| `scan_for_secrets` | Stops execution if secret-like values are present in case files. |
| `run_python_script` | Runs a Python artifact with timeout and captures stdout/stderr. |
| `parse_last_json_object` | Reads the final JSON metric object from script stdout. |
| `compare_metric` | Compares observed metric against the case claim and tolerance. |
| `detect_missing_seed` | Flags obvious randomness without seed control. |
| `detect_data_leakage` | Finds CSV columns that exactly copy the target column. |
| `classify_execution_error` | Turns execution failures into reviewer-friendly findings. |

## Current Verdict Coverage

```bash
PYTHONPATH=src python3 -m reprobench cases audit
```

Expected:

```text
Expected verdicts matched: 5/5
```

## Why This Matters

This milestone moves the project beyond a skeleton. The agent can now produce evidence-backed verdicts for all benchmark cases:

- clean claim reproduced;
- overstated metric rejected;
- missing seed flagged;
- missing dependency classified as blocked;
- target leakage detected even when the metric reproduces.

## Report Export

The core audit workflow can export both Markdown and JSON evidence reports:

```bash
PYTHONPATH=src python3 -m reprobench run examples/cases/data_leakage --output-dir reports/sample/data_leakage
```
