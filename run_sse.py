#!/usr/bin/env python3
"""Run itop-mcp with streamable-http transport for Open WebUI / remote MCP clients.

Required environment variables:
    ITOP_BASE_URL   - URL to your iTop instance (e.g. http://itop.example.com/)
    ITOP_USER       - iTop username
    ITOP_PASSWORD   - iTop password
    ITOP_VERSION    - API version (optional, default: 1.4)
    MCP_HOST        - Host to bind (optional, default: 0.0.0.0)
    MCP_PORT        - Port to listen on (optional, default: 8765)
"""
import os
import sys

for var in ("ITOP_BASE_URL", "ITOP_USER", "ITOP_PASSWORD"):
    if not os.environ.get(var):
        print(f"Error: environment variable {var} is required.", file=sys.stderr)
        sys.exit(1)

import mcp.server.fastmcp as _fmcp
_orig_init = _fmcp.FastMCP.__init__
def _patched_init(self, *args, **kwargs):
    kwargs.pop("description", None)
    kwargs.setdefault("host", os.environ.get("MCP_HOST", "0.0.0.0"))
    kwargs.setdefault("port", int(os.environ.get("MCP_PORT", "8765")))
    _orig_init(self, *args, **kwargs)
_fmcp.FastMCP.__init__ = _patched_init

import main  # noqa: E402

main.mcp.settings.host = os.environ.get("MCP_HOST", "0.0.0.0")
main.mcp.settings.port = int(os.environ.get("MCP_PORT", "8765"))
main.mcp.run(transport="streamable-http")
