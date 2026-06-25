"""Grade, completion, and deadline MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context  # noqa: TC002
from fastmcp.exceptions import ToolError

from moodle_mcp import api
from moodle_mcp.models import (  # noqa: TC001
    CompletionActivity,
    Deadline,
    GradeItem,
    NonEmptyText,
    WriteReceipt,
)
from moodle_mcp.tools.availability import raise_tool_error_for_moodle_failure, require_feature

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Grade and deadline tools."""
    mcp.tool(get_grades)
    mcp.tool(get_course_progress)
    mcp.tool(mark_activity_complete)
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
    feature = api.MoodleFeature.grades
    await require_feature(feature)
    try:
        return await api.get_grades(course_ids, limit)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_course_progress(courseid: int, limit: int = 100) -> list[CompletionActivity]:
    """Return activity completion status for a course.

    Args:
        courseid: The course ID.
    Returns:
        Activities with name, type, completion status, timecompleted.
    """
    feature = api.MoodleFeature.progress
    await require_feature(feature)
    try:
        return await api.get_course_progress(courseid, limit)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def mark_activity_complete(
    cmid: int,
    completed: bool = True,
    dry_run: bool = True,
    reason: NonEmptyText | None = None,
) -> WriteReceipt:
    """Preview or set the completion state of a course activity.

    Use dry_run=True to inspect the intended change without changing Moodle. Use dry_run=False only after the user explicitly confirms and provides reason. Only works for activities with manual completion enabled.

    Args:
        cmid: The course module ID of the activity.
        completed: True to mark complete, False to mark incomplete.
        dry_run: If True, return a preview and do not write to Moodle.
        reason: Human-readable reason required when dry_run is False.
    Returns:
        Activity completion write receipt.
    """
    try:
        if not dry_run:
            await require_feature(api.MoodleFeature.write_completion)
        return await api.mark_activity_complete(cmid, completed, dry_run, reason)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, api.MoodleFeature.write_completion)


async def get_upcoming_deadlines(daysahead: int = 7, limit: int = 50) -> list[Deadline]:
    """Return merged, time-sorted deadlines from assignments and quizzes.

    Args:
        daysahead: How many days ahead to look (default 7).
    Returns:
        Sorted deadlines with type, name, course, duedate, daysremaining.
    """
    feature = api.MoodleFeature.dashboard
    await require_feature(feature)
    try:
        return await api.get_upcoming_deadlines(daysahead, limit)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)
