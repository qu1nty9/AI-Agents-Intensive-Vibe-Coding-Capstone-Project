# ReproBench Agent

[![CI](https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/actions/workflows/ci.yml/badge.svg)](https://github.com/qu1nty9/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/actions/workflows/ci.yml)
[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-2367d1)](https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/)

**ReproBench Agent** is an evidence-first AI agent for checking whether machine learning experiments are reproducible. It reads an experiment case, extracts the claimed result, builds a reproduction plan, runs controlled checks, audits the evidence, and exports a reviewable report.

Kaggle track: **Freestyle**.

> ReproBench Agent turns ML claims into reproducible, auditable evidence.

## Judge This Project In 5 Minutes

Start with the public demo dashboard, then verify the same evidence locally:

1. Open the [GitHub Pages demo](https://qu1nty9.github.io/AI-Agents-Intensive-Vibe-Coding-Capstone-Project/).
2. Review the [judging evidence matrix](docs/evidence_matrix.md).
3. Run the proof path:

```bash
make audit-cases
make sample-report
make mcp-demo
```

Expected proof: benchmark verdicts match `5/5`, the `data_leakage` demo returns `partially_reproduced`, and the MCP demo returns the same structured audit trace.

## Why This Project Exists

Machine learning claims often look convincing until someone tries to rerun the notebook. Missing seeds, hidden preprocessing, metric mismatches, dependency drift, and data leakage can make results unreliable. ReproBench Agent is designed to make those issues visible through an agent workflow with tool calls, traces, and structured reports.

This is built for Kaggle users, reviewers, data scientists, and teams who need fast evidence about whether an experiment claim holds up.

## What The Agent Does

1. Reads a notebook, case spec, or experiment brief.
2. Extracts the claimed metric and assumptions.
3. Builds a reproduction plan.
4. Runs safe, controlled checks through tools.
5. Audits outputs for mismatch, instability, leakage, or blocked execution.
6. Produces a report with verdict, evidence, logs, and recommended fixes.

## Current Status

Milestone 8 is complete: repository foundation, benchmark case suite, local core audit tools, evidence report export, MCP tool wrapper, security hardening, static demo dashboard, final submission docs, and CI-backed proof checks.

Implemented now:

- Python package layout under `src/reprobench`.
- CLI entrypoint.
- Typed domain model for claims, plans, tool calls, findings, and reports.
- Deterministic local audit workflow.
- Five benchmark cases with validated `case.json` specs.
- Local tools for script execution, metric comparison, missing seed detection, leakage detection, secret scanning, and execution error classification.
- `cases audit` command that verifies actual verdicts against expected benchmark verdicts.
- Markdown and JSON report export via `reprobench run --output-dir`.
- Benchmark summary export for Kaggle evidence artifacts.
- MCP-facing tool registry with optional FastMCP server and dependency-free JSON-lines smoke server.
- Security controls for path policy, secret scanning, redaction, and execution timeouts.
- Submission checklist, Mermaid architecture diagram, expanded video script, and writeup draft.
- Final Kaggle writeup and video script drafts.
- Final video plan with the exact on-screen demo path.
- GitHub Actions CI that runs the proof suite on Python 3.11 and 3.12.
- Documentation for architecture, demo, GitHub Pages, security, MCP tools, and Kaggle submission.
- Unit and integration tests for CLI, workflow contracts, tools, reports, and case validation.

Remaining external submission tasks:

- Confirm the latest GitHub Pages workflow is green.
- Record and upload the under-5-minute video.
- Submit the final Kaggle Writeup with Freestyle selected.

## Quickstart

From the repository root:

```bash
PYTHONPATH=src python3 -m reprobench --help
PYTHONPATH=src python3 -m reprobench info
PYTHONPATH=src python3 -m reprobench cases list
PYTHONPATH=src python3 -m reprobench cases validate
PYTHONPATH=src python3 -m reprobench cases audit
PYTHONPATH=src python3 -m reprobench cases audit --output-dir reports/sample/benchmark
PYTHONPATH=src python3 -m reprobench mcp list-tools
PYTHONPATH=src python3 -m reprobench mcp call audit_case --args-json '{"case_path":"examples/cases/data_leakage"}'
PYTHONPATH=src python3 -m reprobench plan examples/cases/clean_baseline
PYTHONPATH=src python3 -m reprobench run examples/cases/clean_baseline
PYTHONPATH=src python3 -m reprobench run examples/cases/data_leakage --output-dir reports/sample/data_leakage
PYTHONPATH=src python3 -m reprobench dashboard
```

After installing the package locally, the console script is also available:

```bash
python3 -m pip install -e .
reprobench --help
```

## Test

The foundation tests use Python's standard library test runner:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Or use the included Makefile:

```bash
make test
make demo
make audit-cases
make benchmark-report
make sample-report
make dashboard
make pages
make mcp-tools
make mcp-demo
make ci
```

If you install the optional development dependencies, `pytest` can also run the same tests:

```bash
pytest
```

## Architecture

The target architecture is a multi-step agent workflow:

- **Coordinator**: owns the run state and delegates work.
- **Claim Extractor**: identifies the claimed metric, dataset, target, and assumptions.
- **Planner**: creates a reproduction protocol.
- **Executor**: invokes tools or MCP tools to inspect and run artifacts.
- **Auditor**: compares observed evidence against claims and looks for failure modes.
- **Reporter**: exports markdown and JSON evidence reports.

More detail: [docs/architecture.md](docs/architecture.md).

MCP details: [docs/mcp_server.md](docs/mcp_server.md).

Security details: [docs/security.md](docs/security.md).

Submission checklist: [docs/submission_checklist.md](docs/submission_checklist.md).

Judging evidence matrix: [docs/evidence_matrix.md](docs/evidence_matrix.md).

Final writeup draft: [docs/kaggle_writeup_final.md](docs/kaggle_writeup_final.md).

Final video script: [docs/video_script_final.md](docs/video_script_final.md).

Full video plan: [docs/video_plan.md](docs/video_plan.md).

Submission bundle: [docs/submission_bundle.md](docs/submission_bundle.md).

Cover image: [docs/assets/reprobench-cover.png](docs/assets/reprobench-cover.png).

Cover source: [docs/assets/reprobench-cover.svg](docs/assets/reprobench-cover.svg).

## Benchmark Suite

The initial benchmark suite lives in [examples/cases](examples/cases). Schema and design rules are documented in [docs/benchmark_cases.md](docs/benchmark_cases.md).

- `clean_baseline`: a valid reproducible experiment.
- `metric_mismatch`: the claimed score is higher than the observed score.
- `seed_instability`: the experiment uses randomness without seed control.
- `missing_dependency`: execution is blocked by an unavailable dependency.
- `data_leakage`: the metric reproduces, but the evidence is compromised by target leakage.

Validate and audit the suite with:

```bash
make validate-cases
make audit-cases
make benchmark-report
```

## Demo Dashboard

Generate the static demo dashboard:

```bash
make dashboard
make pages
```

Open [reports/sample/dashboard/index.html](reports/sample/dashboard/index.html) to inspect the benchmark proof, data leakage verdict, findings, and tool trace in one page.

`make pages` writes the same dashboard to [docs/index.html](docs/index.html), which is ready for GitHub Pages deployment. The dashboard includes benchmark proof, evidence attachments, the judging evidence matrix, audit findings, and the agent tool trace. Deployment notes: [docs/github_pages.md](docs/github_pages.md).

## Repository Layout

```text
.
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── architecture.md
│   ├── demo_script.md
│   ├── kaggle_writeup_draft.md
│   ├── kaggle_writeup_final.md
│   ├── evidence_matrix.md
│   ├── video_plan.md
│   └── video_script_final.md
├── examples/
│   └── cases/
├── reports/
│   └── sample/
├── scripts/
├── src/
│   └── reprobench/
│       ├── agents/
│       ├── benchmark/
│       ├── mcp_server/
│       ├── reporting/
│       ├── security/
│       ├── tools/
│       └── cli.py
└── tests/
```

## Kaggle Submission Strategy

This project is optimized for the judging rubric:

- **Core concept and value**: reproducibility is central to ML and Kaggle work.
- **Video**: show a live case where the agent detects a reproducibility issue.
- **Writeup**: explain why agents are needed for reading, planning, execution, auditing, and reporting.
- **Technical implementation**: expose the agent workflow, tool calls, MCP tools, security layer, and tests.
- **Documentation**: make local setup and demo reproduction straightforward.

## Security Principles

ReproBench Agent must treat notebooks and experiment code as untrusted inputs.

Planned controls:

- no secrets committed to the repository;
- secret scanning before execution;
- command and path allowlists;
- execution timeouts;
- redaction in logs and reports;
- clear unsafe-run verdicts.

## License

MIT.
