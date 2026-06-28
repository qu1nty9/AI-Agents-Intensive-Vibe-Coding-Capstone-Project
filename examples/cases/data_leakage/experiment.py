"""Experiment with intentional target leakage."""

from __future__ import annotations

import csv
import json
from pathlib import Path


def main() -> None:
    dataset_path = Path(__file__).with_name("toy_leakage.csv")
    with dataset_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    labels = [int(row["target"]) for row in rows]
    predictions = [int(row["leaky_target_copy"]) for row in rows]
    correct = sum(int(actual == predicted) for actual, predicted in zip(labels, predictions))
    accuracy = correct / len(labels)

    print(
        json.dumps(
            {
                "metric_name": "accuracy",
                "value": accuracy,
                "n_samples": len(labels),
                "feature_used": "leaky_target_copy",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

