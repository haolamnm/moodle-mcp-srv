"""Assignment MCP resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp import api

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Assignment resources."""
    mcp.resource(
        "moodle://assignments/{assignmentid}/brief",
        name="assignment_brief_resource",
        description="Read-only assignment brief and due-date metadata.",
        mime_type="application/json",
    )(assignment_brief_resource)


async def assignment_brief_resource(assignmentid: int) -> str:
    """Return assignment details as compact JSON resource text."""
    assignment = await api.get_assignment_details(assignmentid)
    if assignment is None:
        return "{}"
    return assignment.model_dump_json()
