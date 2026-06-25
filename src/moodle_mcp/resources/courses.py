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
        "moodle://courses/{courseid}/overview",
        name="course_overview_resource",
        description="Read-only course metadata for an enrolled Moodle course.",
        mime_type="application/json",
    )(course_overview_resource)
    mcp.resource(
        "moodle://courses/{courseid}/assignments",
        name="course_assignments_resource",
        description="Read-only assignments for an enrolled Moodle course.",
        mime_type="application/json",
    )(course_assignments_resource)
    mcp.resource(
        "moodle://grades/{courseid}/schema",
        name="grade_schema_resource",
        description="Read-only grade items visible in a Moodle course.",
        mime_type="application/json",
    )(grade_schema_resource)
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


async def course_overview_resource(courseid: int) -> str:
    """Return course metadata as compact JSON resource text."""
    courses = await api.get_my_courses()
    course = next((item for item in courses if item.id == courseid), None)
    if course is None:
        return "{}"
    return course.model_dump_json()


async def course_assignments_resource(courseid: int) -> str:
    """Return course assignments as compact JSON resource text."""
    assignments = await api.get_assignments([courseid])
    return TypeAdapter(list[api.Assignment]).dump_json(assignments).decode()


async def grade_schema_resource(courseid: int) -> str:
    """Return grade items as compact JSON resource text."""
    grades = await api.get_grades([courseid])
    return TypeAdapter(list[api.GradeItem]).dump_json(grades).decode()


async def dashboard_summary_resource() -> str:
    """Return dashboard summary as compact JSON resource text."""
    return api.DashboardSummary.model_validate(await api.dashboard_summary()).model_dump_json()
