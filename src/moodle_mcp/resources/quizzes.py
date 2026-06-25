"""Quiz MCP resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from moodle_mcp import api

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register quiz-facing resources."""
    mcp.resource(
        "moodle://quizzes/{courseid}/brief",
        name="quiz_brief_resource",
        description="Read-only quiz brief for an enrolled Moodle course.",
        mime_type="application/json",
    )(quiz_brief_resource)


async def quiz_brief_resource(courseid: int) -> str:
    """Return course quizzes as compact JSON resource text."""
    quizzes = await api.get_quizzes([courseid])
    return TypeAdapter(list[api.Quiz]).dump_json(quizzes).decode()
