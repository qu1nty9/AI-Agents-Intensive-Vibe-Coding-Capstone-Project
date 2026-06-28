# Benchmark Cases

This directory contains small reproducibility cases used by the demo and tests.

Implemented cases:

- `clean_baseline`: a valid reproducible experiment.
- `metric_mismatch`: the claimed metric does not match the observed metric.
- `seed_instability`: repeated runs produce unstable results.
- `missing_dependency`: execution is blocked by an environment issue.
- `data_leakage`: a suspiciously strong result is caused by leakage.

Each case includes:

- `case.json`;
- one short script;
- tiny local data, if needed;
- expected verdict;
- explanation for the benchmark.

Validate all cases:

```bash
PYTHONPATH=src python3 -m reprobench cases validate
```

List cases:

```bash
PYTHONPATH=src python3 -m reprobench cases list
```
