# Benchmark Cases

ReproBench uses small controlled cases to prove that the agent can handle both successful and failed reproducibility audits.

Each case lives in `examples/cases/<case_name>/` and must contain `case.json`.

## Current Suite

| Case | Expected Verdict | Purpose |
| --- | --- | --- |
| `clean_baseline` | `reproduced` | Confirms the happy path where the metric matches the claim. |
| `metric_mismatch` | `not_reproduced` | Shows that an overstated metric is rejected. |
| `seed_instability` | `partially_reproduced` | Shows missing seed control and unstable runs. |
| `missing_dependency` | `blocked` | Separates environment failures from disproven claims. |
| `data_leakage` | `partially_reproduced` | Shows that a metric can reproduce while the evidence is compromised. |

## Case Spec

Required fields:

```json
{
  "schema_version": "1.0",
  "name": "case_directory_name",
  "title": "Human-readable case title",
  "description": "What this case demonstrates.",
  "artifact": "experiment.py",
  "claim": {
    "metric_name": "accuracy",
    "expected_value": 0.9,
    "tolerance": 0.0,
    "source": "case_spec"
  },
  "expected_verdict": "reproduced",
  "failure_mode": "none",
  "tags": ["baseline"],
  "checks": ["scan_for_secrets", "run_python_script", "compare_metric"],
  "notes": "Reviewer-facing explanation."
}
```

Optional fields:

- `dataset`: local dataset file used by the artifact.
- `target_column`: target column for leakage checks.

## Validation

```bash
PYTHONPATH=src python3 -m reprobench cases validate
```

Expected output:

```text
Valid cases: 5/5
```

## Design Rules

- Keep cases tiny enough to run during a video demo.
- Use local data only.
- Make the expected verdict explicit.
- Prefer deterministic scripts unless the case is intentionally about instability.
- Keep failure modes intentional and documented.

