# Security Model

ReproBench treats benchmark artifacts as untrusted inputs.

## Implemented Controls

### Path Policy

`case.json` artifact and dataset paths must be relative and must stay inside the case directory.

Blocked examples:

- absolute paths such as `/tmp/script.py`;
- path traversal such as `../outside.py`;
- dataset paths outside the case folder.

The workflow records this check as `validate_path_policy`.

### Secret Scanning

Before execution, ReproBench scans text files for common secret-like values:

- API key assignments;
- OpenAI-style `sk-...` tokens;
- Google API-key-like values;
- AWS access-key-like values;
- private key blocks.

If a secret-like value is found, the verdict becomes `unsafe_to_run`.

### Redaction

stdout, stderr, and parsed JSON output from executed scripts are redacted before they are stored in reports.

The marker is:

```text
[REDACTED]
```

### Execution Boundary

ReproBench currently executes only Python artifacts through `run_python_script`. It does not execute arbitrary shell commands from a case spec.

Execution has a timeout and reports blocked runs separately from disproven claims.

## Demo Commands

```bash
PYTHONPATH=src python3 -m reprobench run examples/cases/data_leakage
PYTHONPATH=src python3 -m reprobench mcp call validate_path_policy --args-json '{"case_path":"examples/cases/data_leakage"}'
```

## Current Limitations

The current sandbox is process-level and lightweight. A stronger production version should run untrusted artifacts inside a container or isolated VM with network controls.

