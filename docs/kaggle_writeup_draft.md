# Kaggle Writeup Draft

## Title

ReproBench Agent: Evidence-First Reproducibility Audits for ML Experiments

## Subtitle

An agent that turns machine learning claims into auditable reproduction reports.

## Problem

Machine learning projects often depend on notebooks, dependencies, random seeds, metrics, and data preparation steps that are difficult to verify quickly. A result can look strong while being fragile, incomplete, or misleading.

## Solution

ReproBench Agent reads an experiment case, extracts the claimed result, plans a reproduction protocol, executes controlled checks through tools, audits the evidence, and exports a structured report.

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

## MCP and Tools

The implementation exposes core capabilities as MCP-facing tools, including case inspection, audit execution, metric comparison, secret scanning, leakage checks, and report export.

## Security

The agent treats notebooks and experiment files as untrusted inputs. Planned controls include secret scanning, path allowlists, execution timeouts, and redaction.

## Evidence

The project includes benchmark cases for clean reproducibility, missing dependencies, random seed instability, metric mismatch, and data leakage.

## Limitations

The initial benchmark is intentionally small and controlled. The project prioritizes transparent evidence and reproducible demos over broad support for arbitrary repositories.
