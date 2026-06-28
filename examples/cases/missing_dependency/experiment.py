"""Experiment that is intentionally blocked by a missing dependency."""

from __future__ import annotations

import json

import definitely_missing_reprobench_dependency


def main() -> None:
    print(
        json.dumps(
            {
                "metric_name": "accuracy",
                "value": definitely_missing_reprobench_dependency.score(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

