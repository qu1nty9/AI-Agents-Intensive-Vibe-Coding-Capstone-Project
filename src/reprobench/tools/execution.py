"""Controlled execution tools for benchmark artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from reprobench.models import ExecutionResult
from reprobench.security import redact_text, redact_value


def run_python_script(script_path: Path, timeout_seconds: int = 120) -> ExecutionResult:
    """Run a Python script and parse the last JSON object printed to stdout."""

    resolved = Path(script_path).resolve()
    command = (sys.executable, str(resolved))
    started_at = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=str(resolved.parent),
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started_at
        return ExecutionResult(
            command=command,
            return_code=124,
            stdout=redact_text(exc.stdout or ""),
            stderr=redact_text(exc.stderr or ""),
            duration_seconds=duration,
            timed_out=True,
            parsed_output=None,
        )

    duration = time.monotonic() - started_at
    parsed_output = parse_last_json_object(completed.stdout)
    return ExecutionResult(
        command=command,
        return_code=completed.returncode,
        stdout=redact_text(completed.stdout),
        stderr=redact_text(completed.stderr),
        duration_seconds=duration,
        timed_out=False,
        parsed_output=redact_value(parsed_output) if parsed_output is not None else None,
    )


def parse_last_json_object(stdout: str) -> dict[str, Any] | None:
    """Parse the last non-empty stdout line as JSON if possible."""

    for line in reversed([line.strip() for line in stdout.splitlines() if line.strip()]):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None
