"""Optional FastMCP server for ReproBench tools."""

from __future__ import annotations

from reprobench.mcp_server.tools import call_tool


def build_server():
    """Build a FastMCP server when the optional MCP SDK is installed."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - depends on optional package
        raise RuntimeError(
            "The MCP SDK is not installed. Install with `python3 -m pip install -e .[mcp]` "
            "or use `reprobench mcp serve-json` for the dependency-free smoke server."
        ) from exc

    mcp = FastMCP("reprobench-agent")

    @mcp.tool()
    def inspect_case(case_path: str) -> dict:
        """Load and return normalized metadata for a ReproBench benchmark case."""

        return call_tool("inspect_case", {"case_path": case_path})

    @mcp.tool()
    def audit_case(case_path: str) -> dict:
        """Run the ReproBench audit workflow for a benchmark case."""

        return call_tool("audit_case", {"case_path": case_path})

    @mcp.tool()
    def run_case_artifact(script_path: str, timeout_seconds: int = 120) -> dict:
        """Run a Python experiment artifact and parse JSON metric output."""

        return call_tool(
            "run_case_artifact",
            {"script_path": script_path, "timeout_seconds": timeout_seconds},
        )

    @mcp.tool()
    def compare_claim_metric(
        metric_name: str,
        expected_value: float,
        actual_value: float,
        tolerance: float = 0.0,
        observed_metric_name: str | None = None,
    ) -> dict:
        """Compare expected and observed metric values within tolerance."""

        return call_tool(
            "compare_claim_metric",
            {
                "metric_name": metric_name,
                "expected_value": expected_value,
                "actual_value": actual_value,
                "tolerance": tolerance,
                "observed_metric_name": observed_metric_name or metric_name,
            },
        )

    @mcp.tool()
    def detect_seed_issue(script_path: str) -> dict:
        """Detect obvious randomness without seed control in a Python artifact."""

        return call_tool("detect_seed_issue", {"script_path": script_path})

    @mcp.tool()
    def detect_leakage(dataset_path: str, target_column: str) -> dict:
        """Detect simple CSV target leakage patterns."""

        return call_tool(
            "detect_leakage",
            {"dataset_path": dataset_path, "target_column": target_column},
        )

    @mcp.tool()
    def scan_case_for_secrets(path: str) -> dict:
        """Scan case files for common secret-like values before execution."""

        return call_tool("scan_case_for_secrets", {"path": path})

    @mcp.tool()
    def export_case_report(case_path: str, output_dir: str) -> dict:
        """Run an audit and export Markdown and JSON report files."""

        return call_tool(
            "export_case_report",
            {"case_path": case_path, "output_dir": output_dir},
        )

    return mcp


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()

