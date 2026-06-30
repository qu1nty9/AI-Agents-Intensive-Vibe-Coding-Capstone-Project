# Judging Evidence Matrix

This matrix maps the strongest ReproBench Agent claims to concrete proof artifacts. Use it as the reviewer-facing index for the Kaggle Freestyle submission.

## Summary

| Judging Claim | Proof Artifact | Verification Command | Status |
| --- | --- | --- | --- |
| The project is an AI agent workflow, not a static report. | `src/reprobench/agents/workflow.py`, `reports/sample/data_leakage/report.md` | `make sample-report` | Complete |
| The agent produces measurable verdicts on controlled cases. | `reports/sample/benchmark/benchmark_summary.md` | `make audit-cases` | Complete |
| The benchmark covers multiple reproducibility failure modes. | `examples/cases/*/case.json`, `docs/benchmark_cases.md` | `make validate-cases` | Complete |
| The data leakage demo separates a reproduced number from trustworthy evidence. | `reports/sample/data_leakage/report.md` | `make sample-report` | Complete |
| The core audit capabilities are available through MCP-facing tools. | `docs/mcp_server.md`, `src/reprobench/mcp_server/tools.py` | `make mcp-demo` | Complete |
| The project treats experiment artifacts as untrusted inputs. | `docs/security.md`, `src/reprobench/security/*` | `make test` | Complete |
| The public demo is generated from committed evidence artifacts. | `docs/index.html`, `reports/sample/dashboard/index.html` | `make pages` | Complete |
| The submission is continuously reproducible. | `.github/workflows/ci.yml`, `.github/workflows/pages.yml` | `make ci` | Complete |

## Evidence By Rubric Lens

### Concept and Usefulness

ReproBench addresses a practical Kaggle problem: a strong score is not enough unless the claim can be reproduced and audited. The dashboard, writeup, and reports all center on the same value proposition: turn ML claims into reproducible evidence.

Proof:

- [Final writeup draft](kaggle_writeup_final.md)
- [Demo dashboard](index.html)
- [Submission bundle](submission_bundle.md)

### Agentic Implementation

The workflow coordinates separate responsibilities: case loading, planning, path validation, secret scanning, leakage detection, execution, metric comparison, and reporting. The value comes from the ordered tool trace and verdict synthesis.

Proof:

- `src/reprobench/agents/workflow.py`
- `src/reprobench/tools/*`
- `reports/sample/data_leakage/report.md`

### Tool and MCP Use

The same audit behavior is exposed through MCP-facing tool definitions and can be invoked through the CLI smoke path. This makes the agent capabilities inspectable instead of hidden behind a one-off script.

Proof:

- [MCP server docs](mcp_server.md)
- `src/reprobench/mcp_server/tools.py`
- `make mcp-demo`

### Evaluation and Reproducibility

The benchmark suite contains five controlled cases with expected verdicts. A successful run must match all expected verdicts, which makes the project judgeable without trusting a narrative alone.

Proof:

- [Benchmark cases](benchmark_cases.md)
- [Benchmark summary](../reports/sample/benchmark/benchmark_summary.md)
- `make audit-cases`

### Safety and Trust

The project includes path policy checks, secret scanning, output redaction, execution timeouts, and blocked/unsafe verdicts. These controls are important because experiment artifacts are treated as untrusted inputs.

Proof:

- [Security model](security.md)
- `tests/unit/test_security.py`
- `tests/unit/test_tools.py`

### Demo Quality

The strongest demo is intentionally narrow and clear: `data_leakage` reports a perfect metric, the metric reproduces, but the evidence is compromised by target leakage. This creates a memorable judging story.

Proof:

- [Final video script](video_script_final.md)
- [Full video plan](video_plan.md)
- [Data leakage evidence report](../reports/sample/data_leakage/report.md)
- [Demo dashboard](index.html)

## Final Submission Check

Run this before the final Kaggle submit:

```bash
make ci
make audit-cases
make sample-report
make pages
make mcp-demo
```

Expected result: tests pass, benchmark verdicts match `5/5`, the data leakage verdict is `partially_reproduced`, the dashboard is regenerated, and the MCP demo returns the same structured audit trace.
