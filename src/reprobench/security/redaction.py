"""Redaction helpers for logs and reports."""

from __future__ import annotations

import re
from typing import Any

SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*=\s*['\"][^'\"]{8,}['\"]"),
)

REDACTION_MARKER = "[REDACTED]"


def redact_text(text: str) -> str:
    """Redact common secret-like values from text."""

    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(REDACTION_MARKER, redacted)
    return redacted


def redact_value(value: Any) -> Any:
    """Recursively redact strings inside JSON-like values."""

    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    if isinstance(value, dict):
        return {key: redact_value(item) for key, item in value.items()}
    return value

