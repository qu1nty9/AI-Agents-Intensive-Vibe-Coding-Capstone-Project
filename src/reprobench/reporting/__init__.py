"""Report generation utilities."""

from reprobench.reporting.export import (
    benchmark_summary_to_dict,
    benchmark_summary_to_markdown,
    report_to_dict,
    report_to_markdown,
    write_benchmark_summary,
    write_report_bundle,
)
from reprobench.reporting.dashboard import build_dashboard_html, write_dashboard

__all__ = [
    "benchmark_summary_to_dict",
    "benchmark_summary_to_markdown",
    "build_dashboard_html",
    "report_to_dict",
    "report_to_markdown",
    "write_benchmark_summary",
    "write_dashboard",
    "write_report_bundle",
]
