"""Assignment MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp.exceptions import ToolError

from moodle_mcp import api
from moodle_mcp.models import (  # noqa: TC001
    Assignment,
    AssignmentFile,
    FeedbackGrade,
    NonEmptyHtml,
    NonEmptyText,
    SubmissionStatus,
    WriteReceipt,
)
from moodle_mcp.tools.availability import raise_tool_error_for_moodle_failure, require_feature

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Assignment tools."""
    mcp.tool(get_assignments)
    mcp.tool(get_assignment_details)
    mcp.tool(get_assignment_files)
    mcp.tool(submit_assignment)
    mcp.tool(check_submission)
    mcp.tool(get_feedback)


async def get_assignments(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[Assignment]:
    """List assignments visible to the current user.

    Args:
        course_ids: Optional list of course IDs to filter by.
        limit: Maximum assignments to return, capped server-side.
    Returns:
        Assignments with id, name, duedate, cutoffdate, grade, intro.
    """
    feature = api.MoodleFeature.assignments
    await require_feature(feature)
    try:
        return await api.get_assignments(course_ids, limit)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_assignment_details(assignmentid: int) -> Assignment | None:
    """Return full details for a single assignment.

    Args:
        assignmentid: The assignment ID.
    Returns:
        Full assignment details including description, submission type, grade.
    """
    feature = api.MoodleFeature.assignments
    await require_feature(feature)
    try:
        return await api.get_assignment_details(assignmentid)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_assignment_files(assignmentid: int) -> list[AssignmentFile]:
    """Return attached files for an assignment.

    Args:
        assignmentid: The assignment ID.
    Returns:
        Attached files with filename, size, mimetype, download URL.
    """
    feature = api.MoodleFeature.assignments
    await require_feature(feature)
    try:
        return await api.get_assignment_files(assignmentid)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def submit_assignment(
    assignmentid: int,
    text: NonEmptyHtml | None = None,
    draft: bool = False,
    dry_run: bool = True,
    reason: NonEmptyText | None = None,
) -> WriteReceipt:
    """Preview or submit an online-text assignment.

    Use dry_run=True to inspect the intended submission without changing Moodle.
    Use dry_run=False only after the user explicitly confirms the submission and provides reason.

    Args:
        assignmentid: The assignment ID.
        text: Optional text submission content.
        draft: If True, save as draft instead of submitting.
        dry_run: If True, return a preview receipt and do not write to Moodle.
        reason: Human-readable reason required when dry_run is False.
    Returns:
        Submission receipt with status.
    """
    try:
        if not dry_run:
            await require_feature(api.MoodleFeature.write_assignment)
        return await api.submit_assignment(assignmentid, text, draft, dry_run, reason)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, api.MoodleFeature.write_assignment)


async def check_submission(assignmentid: int) -> SubmissionStatus:
    """Check submission status for an assignment.

    Args:
        assignmentid: The assignment ID.
    Returns:
        Status (submitted/draft/noattempt), timemodified, grading status.
    """
    feature = api.MoodleFeature.assignment_submission
    await require_feature(feature)
    try:
        return await api.check_submission(assignmentid)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)


async def get_feedback(assignmentid: int) -> FeedbackGrade:
    """Return grade and feedback comments for an assignment.

    Args:
        assignmentid: The assignment ID.
    Returns:
        Grade, feedback text, grader info, timemodified.
    """
    feature = api.MoodleFeature.assignment_submission
    await require_feature(feature)
    try:
        return await api.get_feedback(assignmentid)
    except api.MoodleAPIError as exc:
        raise_tool_error_for_moodle_failure(exc, feature)
