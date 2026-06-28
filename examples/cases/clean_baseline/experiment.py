"""Deterministic baseline experiment for ReproBench Agent."""

from __future__ import annotations

import json


def main() -> None:
    labels = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
    predictions = [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    correct = sum(int(actual == predicted) for actual, predicted in zip(labels, predictions))
    accuracy = correct / len(labels)

    print(
        json.dumps(
            {
                "metric_name": "accuracy",
                "value": accuracy,
                "n_samples": len(labels),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

