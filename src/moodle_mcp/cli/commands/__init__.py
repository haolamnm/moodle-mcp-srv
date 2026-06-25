"""CLI command exports."""

from __future__ import annotations

from moodle_mcp.cli.commands.diagnostics import doctor, ping
from moodle_mcp.cli.commands.inspection import inspect_server
from moodle_mcp.cli.commands.serve import serve

__all__ = ["doctor", "inspect_server", "ping", "serve"]
