"""Grade, completion, and deadline MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context  # noqa: TC002

from moodle_mcp import api
from moodle_mcp.models import CompletionActivity, Deadline, GradeItem  # noqa: TC001

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Grade and deadline tools."""
    mcp.tool(get_grades)
    mcp.tool(get_course_progress)
    mcp.tool(get_upcoming_deadlines)


async def get_grades(
    course_ids: list[int] | None = None,
    limit: int = 100,
    ctx: Context | None = None,
) -> list[GradeItem]:
    """List grade items visible to the current user.

    Use this for grade questions. Do not use it to inspect assignment text, quiz reviews, or course modules.

    Args:
        course_ids: Optional list of course IDs to filter by.
        limit: Maximum grade items to return, capped server-side.
    Returns:
        Grade items with name, raw/percentage/letter grade, range, feedback.
    """
    if ctx is not None:
        await ctx.info("Fetching Moodle grade items")
        await ctx.report_progress(0.2, total=1.0, message="Fetching grades")
    return await api.get_grades(course_ids, limit)


async def get_course_progress(courseid: int, limit: int = 100) -> list[CompletionActivity]:
    """Return activity completion status for a course.

    Args:
        courseid: The course ID.
    Returns:
        Activities with name, type, completion status, timecompleted.
    """
    return await api.get_course_progress(courseid, limit)


async def get_upcoming_deadlines(daysahead: int = 7, limit: int = 50) -> list[Deadline]:
    """Return merged, time-sorted deadlines from assignments and quizzes.

    Args:
        daysahead: How many days ahead to look (default 7).
    Returns:
        Sorted deadlines with type, name, course, duedate, daysremaining.
    """
    return await api.get_upcoming_deadlines(daysahead, limit)
