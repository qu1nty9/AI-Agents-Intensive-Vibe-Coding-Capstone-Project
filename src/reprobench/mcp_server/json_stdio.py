"""Tiny JSON-lines stdio server for exercising MCP-style tool contracts.

This is not a replacement for the official MCP SDK. It is a dependency-free
smoke path that supports the same tool registry used by the optional FastMCP
server.
"""

from __future__ import annotations

import json
import sys
from typing import TextIO

from reprobench.mcp_server.tools import call_tool, list_tools


def serve_json_stdio(stdin: TextIO | None = None, stdout: TextIO | None = None) -> int:
    """Serve simple JSON requests over stdin/stdout.

    Supported methods:

    - `tools/list`
    - `tools/call` with params `{ "name": "...", "arguments": { ... } }`
    """

    input_stream = stdin or sys.stdin
    output_stream = stdout or sys.stdout
    for line in input_stream:
        if not line.strip():
            continue
        response = handle_request(line)
        output_stream.write(json.dumps(response, sort_keys=True) + "\n")
        output_stream.flush()
    return 0


def handle_request(line: str) -> dict:
    try:
        request = json.loads(line)
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params") or {}
        if method == "tools/list":
            return {"id": request_id, "result": {"tools": list_tools()}}
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            return {"id": request_id, "result": call_tool(name, arguments)}
        return {"id": request_id, "error": {"message": f"unknown method: {method}"}}
    except Exception as exc:  # pragma: no cover - intentionally defensive server boundary
        return {"id": None, "error": {"message": str(exc)}}

