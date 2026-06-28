# ReproBench Agent

**ReproBench Agent** is an evidence-first AI agent for checking whether machine learning experiments are reproducible. It reads an experiment case, extracts the claimed result, builds a reproduction plan, runs controlled checks, audits the evidence, and exports a reviewable report.

Kaggle track: **Freestyle**.

> ReproBench Agent turns ML claims into reproducible, auditable evidence.

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

Milestone 0 is complete: repository foundation, package skeleton, CLI, docs, and smoke tests.

Implemented now:

- Python package layout under `src/reprobench`.
- CLI entrypoint.
- Typed domain model for claims, plans, tool calls, findings, and reports.
- Deterministic placeholder workflow.
- Documentation skeleton for architecture, demo, and Kaggle writeup.
- Unit tests for CLI and workflow contracts.

Coming next:

- Benchmark cases in `examples/cases/`.
- Notebook inspection and execution tools.
- Evidence report generation.
- MCP server wrapper for core tools.
- Security layer for untrusted experiment execution.

## Quickstart

From the repository root:

```bash
PYTHONPATH=src python3 -m reprobench --help
PYTHONPATH=src python3 -m reprobench info
PYTHONPATH=src python3 -m reprobench plan examples/cases/clean_baseline
PYTHONPATH=src python3 -m reprobench run examples/cases/clean_baseline
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

## Repository Layout

```text
.
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── architecture.md
│   ├── demo_script.md
│   └── kaggle_writeup_draft.md
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
