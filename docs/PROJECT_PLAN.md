# ReproBench Agent Project Plan

## Project Thesis

Build **ReproBench Agent**, an evidence-first AI agent that verifies whether machine learning experiments are reproducible. The agent takes a notebook, repository, or experiment brief, extracts the claimed result, builds a reproduction plan, runs controlled checks, audits the outputs, and produces a structured evidence report.

Target Kaggle track: **Freestyle**.

Core positioning:

> ReproBench Agent turns "trust me, it works" ML claims into reproducible, auditable evidence.

This should feel like more than an LLM wrapper. The project must demonstrate agentic planning, tool use, execution, security controls, and verifiable outputs.

## Why This Can Be a Strong Freestyle Submission

The project is aligned with the Kaggle audience: notebooks, experiments, metrics, data leakage, reproducibility, and public code. It is also easy to prove in a demo because the agent produces objective artifacts:

- extracted experiment claims;
- reproduction plan;
- tool-call trace;
- notebook execution logs;
- metric comparison;
- issue diagnosis;
- reproducibility verdict;
- exported report;
- benchmark case results.

The key advantage is evidence. The submission should not ask judges to believe that the agent is useful; it should show repeatable runs against intentionally designed benchmark cases.

## Ideal Outcome

By the submission deadline, the repository should contain:

- a working agentic app or CLI demo;
- a small benchmark suite of reproducibility cases;
- an MCP server exposing reproducibility tools;
- multi-agent orchestration or a clearly separated agent workflow;
- security controls for code execution and secret handling;
- reproducible local setup instructions;
- screenshots, architecture diagrams, and generated reports;
- a concise 5-minute YouTube demo;
- a Kaggle Writeup under 2,500 words.

## Current Implementation Status

As of June 29, 2026, the project has progressed beyond the original foundation plan:

- five benchmark cases are implemented and audited with `5/5` expected verdicts matched;
- local tools cover execution, metric comparison, seed checks, leakage checks, secret scanning, redaction, and path policy;
- the agent workflow exports Markdown and JSON evidence reports;
- MCP-facing tools are available through a dependency-free JSON-lines server and optional FastMCP entrypoint;
- security tests cover path traversal, secret handling, redaction, and unsafe-run behavior;
- static dashboard artifacts are generated for local demo and GitHub Pages;
- final writeup and video script drafts are available in `docs/`;
- GitHub Actions CI runs the proof suite on Python 3.11 and Python 3.12.

Deadline from the local competition brief:

- Kaggle submission due: **July 6, 2026 at 11:59 PM PT**.
- Moscow time: **July 7, 2026 at 09:59 MSK**.

## Judging Strategy

The project should optimize for the rubric rather than just feature count.

### Pitch: Problem, Solution, Value - 30 points

What judges should understand in the first 30 seconds:

- ML reproducibility is a real problem.
- Kaggle users, researchers, and teams need fast evidence about whether a notebook or experiment claim holds up.
- Agents are useful here because the task requires reading, planning, running tools, inspecting outputs, adapting, and producing an auditable final answer.

Deliverables:

- clear tagline;
- concise problem statement;
- concrete demo case;
- visible before/after comparison;
- strong final report artifact.

### Implementation: Architecture, Code - 70 points

The implementation must make the agent architecture visible:

- separate planner, executor, auditor, and reporter responsibilities;
- explicit tools rather than hidden helper calls;
- trace logs for every meaningful step;
- deterministic benchmark cases;
- test coverage for core tools;
- security restrictions around execution;
- reproducible setup.

## Required Course Concepts to Demonstrate

The project should explicitly demonstrate at least these concepts:

1. **Agent or multi-agent system**
   - Coordinator agent delegates to extraction, planning, execution, audit, and reporting components.

2. **MCP server**
   - Tools for notebook inspection, controlled execution, metric comparison, leakage checks, report export, and trace export.

3. **Security features**
   - Secret scanning, command allowlist, workspace isolation, execution timeouts, redaction of sensitive values, and transparent tool permissions.

4. **Deployability**
   - Local CLI plus optional lightweight web UI.
   - Docker or clearly reproducible environment instructions.

5. **Agent skills / CLI workflow**
   - `reprobench run <case>` and `reprobench report <run_id>` style commands.

If Antigravity is required or helpful for the course story, show it in the video as the development/demo environment, not as a dependency of the final product.

## Product Scope

### Core User Story

As a data scientist, reviewer, or Kaggle participant, I want to give an agent a notebook and an expected claim so that it can independently check reproducibility and tell me what evidence supports or contradicts the claim.

### Primary Demo Flow

1. User selects a benchmark case.
2. Agent reads the notebook and metadata.
3. Agent extracts the claimed metric and experiment assumptions.
4. Agent creates a reproduction plan.
5. Agent invokes MCP tools to inspect and run the notebook.
6. Agent compares observed metrics against expected metrics.
7. Agent audits failure modes such as missing seed, dependency issue, metric mismatch, or leakage.
8. Agent exports a report with verdict, evidence, logs, and recommended fixes.

### Output Verdicts

- `reproduced`
- `partially_reproduced`
- `not_reproduced`
- `blocked`
- `unsafe_to_run`

## Benchmark Cases

Create a small controlled benchmark in `examples/cases/`.

### Case 1: Clean Reproducible Baseline

Purpose: prove the agent can confirm a valid claim.

Expected result:

- notebook runs;
- metric matches tolerance;
- verdict is `reproduced`.

### Case 2: Missing Dependency

Purpose: prove the agent can diagnose environment problems.

Expected result:

- execution fails;
- dependency is identified;
- verdict is `blocked`;
- report includes install/setup recommendation.

### Case 3: Random Seed Instability

Purpose: prove the agent can detect non-determinism.

Expected result:

- repeated runs produce variable metrics;
- agent flags missing or unstable seed;
- verdict is `partially_reproduced`.

### Case 4: Metric Mismatch

Purpose: prove the agent can detect when a claim uses the wrong metric or threshold.

Expected result:

- notebook runs;
- observed metric differs from claimed metric;
- report explains mismatch.

### Case 5: Data Leakage

Purpose: strongest demo case.

Expected result:

- initial score looks high;
- auditor detects suspicious leakage pattern;
- report downgrades trust in the result.

## Architecture

### Components

#### Coordinator

Owns the workflow:

- receives task;
- selects tools;
- maintains run state;
- delegates to specialized components;
- decides final verdict.

#### Claim Extractor

Finds:

- claimed metric;
- dataset;
- target column;
- train/test split assumptions;
- required dependencies;
- execution entrypoint.

#### Reproduction Planner

Produces:

- run protocol;
- expected artifacts;
- metrics to collect;
- safety constraints;
- fallback checks.

#### Execution Agent

Uses MCP tools to:

- inspect notebooks;
- run notebooks or scripts;
- capture logs;
- collect generated artifacts;
- enforce timeouts.

#### Evidence Auditor

Checks:

- metric agreement;
- missing seeds;
- dependency failures;
- leakage indicators;
- suspicious preprocessing;
- incomplete outputs.

#### Report Generator

Exports:

- markdown report;
- JSON run summary;
- trace log;
- optional HTML report.

### MCP Tools

Initial tool list:

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

### Data Model

Core entities:

- `CaseSpec`
- `Claim`
- `ReproductionPlan`
- `ToolCall`
- `ExecutionResult`
- `AuditFinding`
- `Verdict`
- `EvidenceReport`

## Proposed Repository Structure

```text
.
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── architecture.md
│   ├── kaggle_writeup_draft.md
│   ├── kaggle_writeup_final.md
│   ├── demo_script.md
│   └── video_script_final.md
├── examples/
│   └── cases/
│       ├── clean_baseline/
│       ├── missing_dependency/
│       ├── seed_instability/
│       ├── metric_mismatch/
│       └── data_leakage/
├── reports/
│   └── sample/
├── src/
│   └── reprobench/
│       ├── agents/
│       ├── mcp_server/
│       ├── tools/
│       ├── security/
│       ├── reporting/
│       ├── benchmark/
│       └── cli.py
├── tests/
│   ├── unit/
│   └── integration/
└── scripts/
    ├── run_demo.sh
    └── generate_sample_reports.sh
```

## Technical Stack

Preferred baseline:

- Python 3.11+;
- Typer or Click for CLI;
- Pydantic for typed schemas;
- nbformat / nbclient for notebook inspection and execution;
- pandas / scikit-learn for benchmark cases;
- pytest for tests;
- FastAPI or Streamlit only if a web UI is worth the time;
- MCP Python SDK if dependency setup is practical.

If Google ADK setup is stable in the environment, use it for the visible agent workflow. If not, implement a clean local orchestrator with explicit agent roles and document the tradeoff.

## Security Design

Minimum security features:

- no API keys in repository;
- `.env.example` only;
- secret scanner before execution;
- command allowlist;
- restricted working directory for benchmark runs;
- timeout for notebook/script execution;
- redaction in logs and reports;
- clear warning for untrusted notebooks.

Stretch security features:

- Dockerized sandbox;
- network-disabled execution profile;
- file access policy;
- report section explaining unsafe operations that were blocked.

## Implementation Milestones

### Milestone 0: Repository Foundation

Goal: make the repo professional before feature work.

Deliverables:

- README with project thesis and quickstart;
- `pyproject.toml`;
- package skeleton;
- `.gitignore`;
- `.env.example`;
- initial docs;
- local test command.

Acceptance criteria:

- `pytest` runs;
- `python -m reprobench --help` or equivalent works;
- README explains what the project is in under 60 seconds.

### Milestone 1: Benchmark Cases

Goal: create controlled cases that prove the value.

Deliverables:

- 3 initial cases: clean baseline, metric mismatch, seed instability;
- metadata file per case;
- expected verdict per case;
- tiny datasets generated locally or committed as small CSV files.

Acceptance criteria:

- each case can be run manually;
- expected outcomes are documented;
- no large data files.

### Milestone 2: Core Tooling

Goal: tools work before agents are layered on top.

Deliverables:

- notebook inspector;
- notebook runner;
- metric comparator;
- seed detector;
- report writer;
- trace logger.

Acceptance criteria:

- unit tests for each tool;
- integration test for one full case;
- sample report generated.

### Milestone 3: Agent Workflow

Goal: implement the actual agentic flow.

Deliverables:

- coordinator;
- claim extraction;
- planning;
- execution;
- audit;
- reporting;
- visible run trace.

Acceptance criteria:

- `reprobench run examples/cases/clean_baseline` produces a valid report;
- trace shows decisions and tool calls;
- final verdict matches expected case metadata.

### Milestone 4: MCP Server

Goal: expose core capabilities as MCP tools.

Deliverables:

- MCP server entrypoint;
- tool schemas;
- README section for using MCP;
- demo using at least 3 MCP tools.

Acceptance criteria:

- MCP server starts locally;
- tools return structured JSON;
- demo trace references MCP tool calls.

### Milestone 5: Security Layer

Goal: make safety visible and judgeable.

Deliverables:

- secret scan;
- command/path allowlist;
- timeout controls;
- redaction;
- unsafe case demo if time allows.

Acceptance criteria:

- test proving a secret is redacted;
- test proving unsafe path/command is blocked;
- report includes security section.

### Milestone 6: Polish and Demo UX

Goal: make the project understandable fast.

Deliverables:

- polished CLI output;
- optional lightweight UI;
- generated sample reports;
- architecture diagram;
- screenshots or GIF;
- demo script.

Acceptance criteria:

- a reviewer can run the demo from README;
- the demo completes in under 3 minutes locally;
- output is visually clear enough for video.

### Milestone 7: Submission Package

Goal: prepare Kaggle submission assets.

Deliverables:

- Kaggle Writeup draft under 2,500 words;
- YouTube video outline and recording;
- cover image;
- public GitHub repo;
- final project link.

Acceptance criteria:

- all links public;
- no secrets;
- README setup verified from clean checkout;
- writeup maps explicitly to judging criteria.

### Milestone 8: CI-Backed Proof Package

Goal: make the submission evidence continuously verifiable.

Deliverables:

- GitHub Actions CI workflow;
- `make ci` local proof command;
- generated benchmark, report, dashboard, and Pages artifacts checked for drift;
- README badges and final submission links.

Acceptance criteria:

- CI passes on Python 3.11 and Python 3.12;
- `make ci` passes locally;
- generated evidence artifacts stay in sync with the committed outputs.

## Timeline

### June 28, 2026

- Finalize project plan.
- Build repository foundation.
- Create package skeleton and README.

### June 29, 2026

- Implement benchmark cases.
- Implement notebook inspection and execution tools.

### June 30, 2026

- Implement agent workflow.
- Generate first full evidence report.

### July 1, 2026

- Add MCP server.
- Add structured traces and report export.

### July 2, 2026

- Add security layer.
- Add tests for security and core tools.

### July 3, 2026

- Polish CLI and optional UI.
- Generate sample reports and screenshots.

### July 4, 2026

- Draft Kaggle Writeup.
- Create architecture diagrams.
- Prepare video script.

### July 5, 2026

- Record and edit video.
- Verify public repo and setup from scratch.

### July 6, 2026

- Final submission QA.
- Submit before the Kaggle deadline.

## Definition of Done

The project is submission-ready when all of these are true:

- `README.md` explains the project, setup, architecture, and demo.
- The agent can run at least 4 benchmark cases.
- At least 3 cases produce correct expected verdicts.
- At least 1 case demonstrates a non-trivial failure diagnosis.
- MCP tools are implemented or clearly documented with a working local demo.
- Security features are implemented and tested.
- Reports are exported as markdown and JSON.
- Tests pass.
- CI passes on GitHub.
- No secrets are present in the repository.
- Public video is under 5 minutes.
- Kaggle Writeup is under 2,500 words.

## Main Risks

### Risk: Too Much Scope

Mitigation:

- CLI first, UI optional.
- Use small synthetic benchmark cases.
- Prioritize evidence reports over visual polish.

### Risk: Agent Looks Like a Wrapper

Mitigation:

- expose planning;
- show tool calls;
- include adaptive behavior;
- include failure diagnosis;
- include benchmark results.

### Risk: MCP or ADK Setup Consumes Too Much Time

Mitigation:

- design tools as plain Python functions first;
- wrap stable tools with MCP after core behavior works;
- document any environment tradeoffs honestly.

### Risk: Reproducibility Demo Is Slow

Mitigation:

- use tiny datasets;
- keep notebooks short;
- cache generated sample reports for video;
- keep live demo path under 3 minutes.

## Final Video Structure

Target duration: 4:30 to 5:00.

1. 0:00-0:30 - Problem and project thesis.
2. 0:30-1:00 - Why agents are needed.
3. 1:00-1:40 - Architecture diagram.
4. 1:40-3:30 - Live demo on one strong benchmark case.
5. 3:30-4:20 - Evidence report, traces, security features.
6. 4:20-5:00 - What was built, what works, why it matters.

## Kaggle Writeup Structure

Target length: 1,800-2,200 words.

1. Title and subtitle.
2. Problem statement.
3. Why this needs an agent.
4. System architecture.
5. MCP tools and execution workflow.
6. Security model.
7. Benchmark cases and evidence.
8. Demo and repository links.
9. Limitations and future work.

## North Star

The final project should make one thing obvious:

> ReproBench Agent does not just answer questions about ML reproducibility. It gathers evidence, runs checks, audits results, and produces a reviewable report.
