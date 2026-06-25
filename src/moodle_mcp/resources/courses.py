"""Course and dashboard MCP resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from moodle_mcp import api

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register course-facing resources."""
    mcp.resource(
        "moodle://courses/{courseid}/content",
        name="course_content_resource",
        description="Read-only course sections and modules for a Moodle course.",
        mime_type="application/json",
    )(course_content_resource)
    mcp.resource(
        "moodle://dashboard/summary",
        name="dashboard_summary_resource",
        description="Read-only cross-course dashboard summary for the current Moodle user.",
        mime_type="application/json",
    )(dashboard_summary_resource)


async def course_content_resource(courseid: int) -> str:
    """Return course content as compact JSON resource text."""
    sections = await api.get_course_content(courseid)
    return TypeAdapter(list[api.CourseSection]).dump_json(sections).decode()


async def dashboard_summary_resource() -> str:
    """Return dashboard summary as compact JSON resource text."""
    return api.DashboardSummary.model_validate(await api.dashboard_summary()).model_dump_json()
