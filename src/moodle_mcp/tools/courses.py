"""Course, Calendar Event, and Dashboard Summary MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp import Context  # noqa: TC002

from moodle_mcp import api
from moodle_mcp.models import (  # noqa: TC001
    CalendarEvent,
    Course,
    CourseSection,
    DashboardSummary,
    SiteInfo,
)
from moodle_mcp.tools.availability import raise_tool_error_for_moodle_failure, require_feature

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register course-facing tools."""
    mcp.tool(get_site_info)
    mcp.tool(get_my_courses)
    mcp.tool(get_course_content)
    mcp.tool(get_calendar_events)
    mcp.tool(dashboard_summary)


async def get_site_info() -> SiteInfo:
    """Return authenticated Moodle site and current-user metadata.

    Use this as a lightweight health/capability probe before deeper Moodle calls. Moodle may include release and version when the token's web-service context allows it.
    """
    return await api.get_site_info()


async def get_my_courses() -> list[Course]:
    """Return all courses the current user is enrolled in.

    First thing to run: discovers what semester courses you're taking.
    Resolves the user from the API token automatically.
    """
    feature = api.MoodleFeature.courses
    await require_feature(feature)
    try:
        return await api.get_my_courses()
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_course_content(courseid: int) -> list[CourseSection]:
    """Return sections and modules for a given course.

    Args:
        courseid: Moodle course ID (from get_my_courses).
    Returns:
        Sections with modules (name, modname, url, description).
    """
    feature = api.MoodleFeature.course_content
    await require_feature(feature)
    try:
        return await api.get_course_content(courseid)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_calendar_events(
    daysahead: int = 14,
    limit: int = 50,
) -> list[CalendarEvent]:
    """List upcoming calendar events from enrolled courses.

    Args:
        daysahead: How many days ahead to look (default 14).
        limit: Maximum events to return, capped server-side.
    Returns:
        Events with type, name, description, timestart, course context.
    """
    feature = api.MoodleFeature.calendar
    await require_feature(feature)
    try:
        return await api.get_calendar_events(daysahead, limit)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def dashboard_summary(ctx: Context | None = None) -> DashboardSummary:
    """Build a compact cross-course dashboard summary.

    Use this when the user asks what needs attention across Moodle. Do not use this for full course content, full grade reports, or write actions.
    """
    if ctx is not None:
        await ctx.info("Building Moodle dashboard summary")
        await ctx.report_progress(0.1, total=1.0, message="Fetching courses")
    feature = api.MoodleFeature.dashboard
    await require_feature(feature)
    try:
        return await api.dashboard_summary()
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)
