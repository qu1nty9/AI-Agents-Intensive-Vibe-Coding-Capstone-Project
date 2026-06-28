"""Experiment with missing seed control."""

from __future__ import annotations

import json
import random


def main() -> None:
    labels = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
    predictions = [label if random.random() > 0.18 else 1 - label for label in labels]
    correct = sum(int(actual == predicted) for actual, predicted in zip(labels, predictions))
    accuracy = correct / len(labels)

    print(
        json.dumps(
            {
                "metric_name": "accuracy",
                "value": accuracy,
                "n_samples": len(labels),
                "seed": null_seed_marker(),
            },
            sort_keys=True,
        )
    )


def null_seed_marker() -> None:
    return None


if __name__ == "__main__":
    main()

