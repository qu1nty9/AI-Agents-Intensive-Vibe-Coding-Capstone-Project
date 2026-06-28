# Demo Script

Target video length: under 5 minutes.

## 0:00-0:30 - Problem

Machine learning notebooks often make claims that are hard to verify. A score may depend on a hidden seed, a fragile environment, a metric mismatch, or even data leakage.

## 0:30-1:00 - Solution

ReproBench Agent checks ML experiment reproducibility by reading the case, planning checks, running tools, auditing evidence, and exporting a report.

## 1:00-1:40 - Architecture

Show the architecture diagram:

- Coordinator;
- Claim Extractor;
- Planner;
- Security Guard;
- Executor;
- MCP tools;
- Evidence Auditor;
- Reporter.

## 1:40-3:30 - Live Demo

Recommended final demo case: `data_leakage`.

Show:

```bash
reprobench run examples/cases/data_leakage
```

Then open the generated report and point out:

- extracted claim;
- plan;
- tool trace;
- observed metric;
- leakage finding;
- final verdict;
- recommended fix.

Also show the full benchmark proof:

```bash
reprobench cases audit
```

## 3:30-4:20 - Evidence and Safety

Show sample reports and tests. Mention that untrusted code is treated carefully through secret scanning, allowlists, timeouts, and redaction.

## 4:20-5:00 - Close

State why this matters for Kaggle and ML work:

> ReproBench Agent does not just answer whether a result is believable. It gathers evidence and makes the review reproducible.
