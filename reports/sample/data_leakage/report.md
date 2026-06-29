# ReproBench Evidence Report: data_leakage

**Verdict:** `partially_reproduced`

**Summary:** The metric evidence is incomplete or compromised by audit findings.

## Reproduction Plan

1. Load and validate benchmark case metadata.
2. Inspect case metadata and available experiment artifacts.
3. Extract the claimed metric, expected value, and tolerance.
4. Run safety checks before executing untrusted code.
5. Execute the experiment in a controlled environment.
6. Compare observed evidence against the claim.
7. Export a reproducibility report with trace and findings.

## Safety Checks

- `scan_for_secrets`
- `validate_case_path`
- `validate_path_policy`
- `enforce_execution_timeout`
- `detect_data_leakage`
- `run_python_script`
- `compare_metric`

## Tool Trace

1. `load_case_spec` - **completed**

   ```json
   {"path": "examples/cases/data_leakage"}
   ```
2. `validate_case_path` - **completed**

   ```json
   {"path": "examples/cases/data_leakage"}
   ```
3. `validate_path_policy` - **completed**

   ```json
   {"findings": 0, "path": "examples/cases/data_leakage"}
   ```
4. `scan_for_secrets` - **completed**

   ```json
   {"findings": 0, "path": "examples/cases/data_leakage"}
   ```
5. `detect_data_leakage` - **completed**

   ```json
   {"dataset_path": "examples/cases/data_leakage/toy_leakage.csv", "findings": 1, "target_column": "target"}
   ```
6. `run_python_script` - **completed**

   ```json
   {"path": "examples/cases/data_leakage/experiment.py", "return_code": 0, "run_index": 1, "timed_out": false}
   ```
7. `compare_metric` - **completed**

   ```json
   {"actual": 1.0, "delta": 0.0, "expected": 1.0, "metric_name": "accuracy", "tolerance": 0.0}
   ```

## Findings

- **[info] Loaded benchmark case: Data Leakage:** Expected verdict is partially_reproduced; claim is accuracy=1.0 tolerance=0.0; failure mode is data_leakage.
- **[warning] Potential target leakage:** Column 'leaky_target_copy' exactly matches target column 'target' for all 8 rows.
- **[info] Metric reproduced within tolerance:** accuracy: expected 1.0, observed 1.0, tolerance 0.0.
