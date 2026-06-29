"""Command-line interface for ReproBench Agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reprobench import __version__
from reprobench.agents.workflow import build_initial_plan, run_foundation_workflow
from reprobench.benchmark import list_case_specs, validate_all_cases, validate_case_directory
from reprobench.mcp_server import call_tool, list_tools
from reprobench.mcp_server.json_stdio import serve_json_stdio
from reprobench.reporting import report_to_dict, write_report_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reprobench",
        description="Evidence-first agent for reproducible ML experiment audits.",
    )
    parser.add_argument("--version", action="version", version=f"reprobench {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("info", help="Show project and milestone information.")

    cases_parser = subparsers.add_parser("cases", help="List or validate benchmark cases.")
    cases_subparsers = cases_parser.add_subparsers(dest="cases_command")

    cases_list_parser = cases_subparsers.add_parser("list", help="List discovered benchmark cases.")
    cases_list_parser.add_argument(
        "--root",
        type=Path,
        default=Path("examples/cases"),
        help="Root directory containing benchmark cases.",
    )
    cases_list_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    cases_validate_parser = cases_subparsers.add_parser(
        "validate",
        help="Validate one benchmark case or all discovered cases.",
    )
    cases_validate_parser.add_argument(
        "case_path",
        nargs="?",
        type=Path,
        help="Optional case directory. If omitted, validates all cases.",
    )
    cases_validate_parser.add_argument(
        "--root",
        type=Path,
        default=Path("examples/cases"),
        help="Root directory used when validating all cases.",
    )
    cases_validate_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    cases_audit_parser = cases_subparsers.add_parser(
        "audit",
        help="Run all benchmark cases and compare actual verdicts with expected verdicts.",
    )
    cases_audit_parser.add_argument(
        "--root",
        type=Path,
        default=Path("examples/cases"),
        help="Root directory containing benchmark cases.",
    )
    cases_audit_parser.add_argument("--json", action="store_true", help="Print JSON output.")

    plan_parser = subparsers.add_parser("plan", help="Create a reproduction plan for a case.")
    plan_parser.add_argument("case_path", type=Path, help="Path to an experiment case.")

    run_parser = subparsers.add_parser("run", help="Run the foundation audit workflow.")
    run_parser.add_argument("case_path", type=Path, help="Path to an experiment case.")
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON instead of readable text.",
    )
    run_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Optional directory for writing report.md and report.json.",
    )

    mcp_parser = subparsers.add_parser("mcp", help="Inspect or serve ReproBench MCP tools.")
    mcp_subparsers = mcp_parser.add_subparsers(dest="mcp_command")
    mcp_subparsers.add_parser("list-tools", help="List MCP-exposed tool schemas.")

    mcp_call_parser = mcp_subparsers.add_parser("call", help="Call an MCP-exposed tool.")
    mcp_call_parser.add_argument("tool_name", help="Registered tool name.")
    mcp_call_parser.add_argument(
        "--args-json",
        default="{}",
        help="JSON object passed as tool arguments.",
    )

    mcp_subparsers.add_parser(
        "serve-json",
        help="Run the dependency-free JSON-lines stdio server.",
    )
    mcp_subparsers.add_parser(
        "serve-fastmcp",
        help="Run the optional FastMCP server. Requires installing .[mcp].",
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

    if args.command == "cases":
        return handle_cases_command(args, parser)

    if args.command == "plan":
        plan = build_initial_plan(args.case_path)
        print_plan(plan.case_name, list(plan.steps), list(plan.safety_checks))
        return 0

    if args.command == "run":
        report = run_foundation_workflow(args.case_path)
        if args.output_dir:
            markdown_path, json_path = write_report_bundle(report, args.output_dir)
            print(f"Wrote report: {markdown_path}")
            print(f"Wrote report: {json_path}")
        if args.json:
            print(json.dumps(report_to_dict(report), indent=2))
        else:
            print_report(report)
        return 0

    if args.command == "mcp":
        return handle_mcp_command(args, parser)

    parser.error(f"unknown command: {args.command}")
    return 2


def handle_mcp_command(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    if args.mcp_command is None:
        parser.error("mcp requires a subcommand")

    if args.mcp_command == "list-tools":
        print(json.dumps({"tools": list_tools()}, indent=2))
        return 0

    if args.mcp_command == "call":
        try:
            arguments = json.loads(args.args_json)
        except json.JSONDecodeError as exc:
            parser.error(f"--args-json must be a JSON object: {exc}")
        if not isinstance(arguments, dict):
            parser.error("--args-json must decode to a JSON object")
        print(json.dumps(call_tool(args.tool_name, arguments), indent=2))
        return 0

    if args.mcp_command == "serve-json":
        return serve_json_stdio()

    if args.mcp_command == "serve-fastmcp":
        from reprobench.mcp_server.server import main as mcp_main

        mcp_main()
        return 0

    parser.error(f"unknown mcp subcommand: {args.mcp_command}")
    return 2


def handle_cases_command(args: argparse.Namespace, parser: argparse.ArgumentParser) -> int:
    if args.cases_command is None:
        parser.error("cases requires a subcommand: list or validate")

    if args.cases_command == "list":
        specs = list_case_specs(args.root)
        if args.json:
            print(json.dumps([case_spec_to_dict(spec) for spec in specs], indent=2))
        else:
            print(f"Benchmark cases: {len(specs)}")
            for spec in specs:
                verdict = spec.expected_verdict.value if spec.expected_verdict else "unknown"
                print(f"- {spec.name}: {spec.title} [{verdict}]")
        return 0

    if args.cases_command == "validate":
        results = (
            [validate_case_directory(args.case_path)]
            if args.case_path
            else validate_all_cases(args.root)
        )
        if args.json:
            print(json.dumps([validation_result_to_dict(result) for result in results], indent=2))
        else:
            print_validation_results(results)
        return 0 if all(result.valid for result in results) else 1

    if args.cases_command == "audit":
        rows = []
        for spec in list_case_specs(args.root):
            report = run_foundation_workflow(spec.path)
            expected = spec.expected_verdict.value if spec.expected_verdict else None
            actual = report.verdict.value
            rows.append(
                {
                    "name": spec.name,
                    "expected_verdict": expected,
                    "actual_verdict": actual,
                    "matched": expected == actual,
                }
            )
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print_audit_rows(rows)
        return 0 if all(row["matched"] for row in rows) else 1

    parser.error(f"unknown cases subcommand: {args.cases_command}")
    return 2


def print_info() -> None:
    print("ReproBench Agent")
    print(f"Version: {__version__}")
    print("Track: Kaggle Freestyle")
    print("Milestone: 5 - security hardening")
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


def print_validation_results(results) -> None:
    valid_count = sum(1 for result in results if result.valid)
    print(f"Valid cases: {valid_count}/{len(results)}")
    for result in results:
        status = "valid" if result.valid else "invalid"
        case_name = result.spec.name if result.spec else str(result.case_path)
        print(f"- {case_name}: {status}")
        for error in result.errors:
            print(f"  error: {error}")


def print_audit_rows(rows: list[dict]) -> None:
    matched_count = sum(1 for row in rows if row["matched"])
    print(f"Expected verdicts matched: {matched_count}/{len(rows)}")
    for row in rows:
        status = "ok" if row["matched"] else "mismatch"
        print(
            f"- {row['name']}: expected={row['expected_verdict']} "
            f"actual={row['actual_verdict']} [{status}]"
        )


def case_spec_to_dict(spec) -> dict:
    claim = spec.claim
    return {
        "name": spec.name,
        "title": spec.title,
        "description": spec.description,
        "artifact_path": str(spec.artifact_path) if spec.artifact_path else None,
        "dataset_path": str(spec.dataset_path) if spec.dataset_path else None,
        "target_column": spec.target_column,
        "expected_verdict": spec.expected_verdict.value if spec.expected_verdict else None,
        "failure_mode": spec.failure_mode,
        "tags": list(spec.tags),
        "checks": list(spec.checks),
        "claim": {
            "metric_name": claim.metric_name,
            "expected_value": claim.expected_value,
            "tolerance": claim.tolerance,
            "source": claim.source,
        }
        if claim
        else None,
    }


def validation_result_to_dict(result) -> dict:
    return {
        "case_path": str(result.case_path),
        "valid": result.valid,
        "errors": list(result.errors),
        "spec": case_spec_to_dict(result.spec) if result.spec else None,
    }


if __name__ == "__main__":
    raise SystemExit(main())
