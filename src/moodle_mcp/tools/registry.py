"""FastMCP tool registration grouped by Moodle domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp.tools import assignments, courses, forums, grades, quizzes

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_tools(mcp: FastMCP) -> None:
    """Register all Moodle MCP tools."""
    courses.register(mcp)
    assignments.register(mcp)
    grades.register(mcp)
    quizzes.register(mcp)
    forums.register(mcp)
