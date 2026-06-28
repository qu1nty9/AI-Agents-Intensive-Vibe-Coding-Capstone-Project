"""Command-line interface for ReproBench Agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reprobench import __version__
from reprobench.agents.workflow import build_initial_plan, run_foundation_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reprobench",
        description="Evidence-first agent for reproducible ML experiment audits.",
    )
    parser.add_argument("--version", action="version", version=f"reprobench {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("info", help="Show project and milestone information.")

    plan_parser = subparsers.add_parser("plan", help="Create a reproduction plan for a case.")
    plan_parser.add_argument("case_path", type=Path, help="Path to an experiment case.")

    run_parser = subparsers.add_parser("run", help="Run the foundation audit workflow.")
    run_parser.add_argument("case_path", type=Path, help="Path to an experiment case.")
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON instead of readable text.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "info":
        print_info()
        return 0

    if args.command == "plan":
        plan = build_initial_plan(args.case_path)
        print_plan(plan.case_name, list(plan.steps), list(plan.safety_checks))
        return 0

    if args.command == "run":
        report = run_foundation_workflow(args.case_path)
        if args.json:
            print(json.dumps(report_to_dict(report), indent=2))
        else:
            print_report(report)
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def print_info() -> None:
    print("ReproBench Agent")
    print(f"Version: {__version__}")
    print("Track: Kaggle Freestyle")
    print("Milestone: 0 - repository foundation")
    print("Thesis: Turn ML claims into reproducible, auditable evidence.")


def print_plan(case_name: str, steps: list[str], safety_checks: list[str]) -> None:
    print(f"Case: {case_name}")
    print("Plan:")
    for index, step in enumerate(steps, start=1):
        print(f"  {index}. {step}")
    print("Safety checks:")
    for index, check in enumerate(safety_checks, start=1):
        print(f"  {index}. {check}")


def print_report(report) -> None:
    print(f"Case: {report.case_name}")
    print(f"Verdict: {report.verdict.value}")
    print(f"Summary: {report.summary}")
    print("Tool trace:")
    for index, tool_call in enumerate(report.tool_calls, start=1):
        print(f"  {index}. {tool_call.name} - {tool_call.status}")
    if report.findings:
        print("Findings:")
        for finding in report.findings:
            print(f"  [{finding.severity}] {finding.title}: {finding.detail}")


def report_to_dict(report) -> dict:
    return {
        "case_name": report.case_name,
        "verdict": report.verdict.value,
        "summary": report.summary,
        "plan": {
            "steps": list(report.plan.steps),
            "safety_checks": list(report.plan.safety_checks),
        },
        "tool_calls": [
            {
                "name": tool_call.name,
                "inputs": tool_call.inputs,
                "status": tool_call.status,
            }
            for tool_call in report.tool_calls
        ],
        "findings": [
            {
                "severity": finding.severity,
                "title": finding.title,
                "detail": finding.detail,
            }
            for finding in report.findings
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())

