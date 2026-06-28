# Benchmark Cases

This directory will contain small reproducibility cases used by the demo and tests.

Planned cases:

- `clean_baseline`: a valid reproducible experiment.
- `metric_mismatch`: the claimed metric does not match the observed metric.
- `seed_instability`: repeated runs produce unstable results.
- `missing_dependency`: execution is blocked by an environment issue.
- `data_leakage`: a suspiciously strong result is caused by leakage.

Each case should eventually include:

- `case.yaml` or `case.json`;
- one short notebook or script;
- tiny local data, if needed;
- expected verdict;
- explanation for the benchmark.

