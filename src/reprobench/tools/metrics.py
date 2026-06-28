"""Metric comparison tools."""

from __future__ import annotations

from reprobench.models import Claim, MetricComparison


def compare_metric(claim: Claim, observed: dict) -> MetricComparison:
    """Compare an observed metric dictionary against a claim."""

    metric_name = str(observed.get("metric_name", ""))
    if metric_name != claim.metric_name:
        actual_value = float("nan")
        return MetricComparison(
            metric_name=metric_name,
            expected_value=float(claim.expected_value if claim.expected_value is not None else 0.0),
            actual_value=actual_value,
            tolerance=float(claim.tolerance or 0.0),
            passed=False,
            delta=float("nan"),
        )

    actual_value = float(observed["value"])
    expected_value = float(claim.expected_value if claim.expected_value is not None else 0.0)
    tolerance = float(claim.tolerance or 0.0)
    delta = abs(actual_value - expected_value)
    return MetricComparison(
        metric_name=metric_name,
        expected_value=expected_value,
        actual_value=actual_value,
        tolerance=tolerance,
        passed=delta <= tolerance,
        delta=delta,
    )

