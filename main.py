"""Compatibility wrapper for the Moodle MCP CLI.

Usage:
    moodle-mcp               # Run over stdio (default)
    moodle-mcp --http        # Run over HTTP
    moodle-mcp --http --port 8080
"""

from __future__ import annotations

from moodle_mcp.cli import main

if __name__ == "__main__":
    main()
