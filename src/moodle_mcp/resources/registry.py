"""FastMCP resource registration grouped by Moodle context."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp.resources import assignments, courses, forums, quizzes, site

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """Register all read-only Moodle MCP resources."""
    site.register(mcp)
    courses.register(mcp)
    assignments.register(mcp)
    quizzes.register(mcp)
    forums.register(mcp)
