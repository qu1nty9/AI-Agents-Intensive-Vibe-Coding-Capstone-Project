# MCP Server

ReproBench exposes its core audit capabilities as MCP-facing tools.

The repository supports two paths:

1. **Dependency-free smoke path** for tests, demos, and local development.
2. **Optional FastMCP server** when the MCP Python SDK is installed.

## Tool List

```bash
PYTHONPATH=src python3 -m reprobench mcp list-tools
```

Implemented tools:

- `inspect_case`
- `audit_case`
- `run_case_artifact`
- `compare_claim_metric`
- `detect_seed_issue`
- `detect_leakage`
- `scan_case_for_secrets`
- `validate_path_policy`
- `export_case_report`

## Tool Call Demo

```bash
PYTHONPATH=src python3 -m reprobench mcp call audit_case --args-json '{"case_path":"examples/cases/data_leakage"}'
```

Expected result:

- verdict: `partially_reproduced`;
- leakage finding present;
- metric comparison present;
- tool trace present.

## JSON-Lines Stdio Smoke Server

This server is intentionally small and dependency-free. It exercises the same registry used by the optional FastMCP layer.

```bash
PYTHONPATH=src python3 -m reprobench mcp serve-json
```

Supported request methods:

```json
{"id": 1, "method": "tools/list"}
```

```json
{"id": 2, "method": "tools/call", "params": {"name": "inspect_case", "arguments": {"case_path": "examples/cases/clean_baseline"}}}
```

## Optional FastMCP Server

Install optional dependency:

```bash
python3 -m pip install -e ".[mcp]"
```

Run:

```bash
reprobench-mcp
```

or:

```bash
PYTHONPATH=src python3 -m reprobench mcp serve-fastmcp
```

If the MCP SDK is not installed, the command fails with an explicit setup message.
