"""Forum and Announcement MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastmcp.exceptions import ToolError

from moodle_mcp import api
from moodle_mcp.models import AnnouncementPost, ForumDiscussion, ForumPost  # noqa: TC001

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Forum and Announcement tools."""
    mcp.tool(get_forum_discussions)
    mcp.tool(post_forum_reply)
    mcp.tool(create_forum_discussion)
    mcp.tool(get_announcements)


async def get_forum_discussions(
    courseid: int,
    forumid: int | None = None,
    limit: int = 50,
) -> list[ForumDiscussion]:
    """List forum discussions in a course.

    Args:
        courseid: The course ID.
        forumid: Optional forum ID to filter by.
        limit: Maximum discussions to return, capped server-side.
    Returns:
        Discussions with name, author, timemodified, post count.
    """
    return await api.get_forum_discussions(courseid, forumid, limit)


async def post_forum_reply(
    discussionid: int,
    message: str,
    subject: str | None = None,
    dry_run: bool = True,
    reason: str | None = None,
) -> ForumPost:
    """Preview or post a forum reply.

    Use dry_run=True to inspect the intended reply without changing Moodle. Use dry_run=False only after the user explicitly confirms the post and provides reason.

    Args:
        discussionid: The discussion ID.
        message: The reply content (HTML).
        subject: Optional subject line.
        dry_run: If True, return a preview and do not write to Moodle.
        reason: Human-readable reason required when dry_run is False.
    Returns:
        Post id and timestamp.
    """
    try:
        return await api.post_forum_reply(discussionid, message, subject, dry_run, reason)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


async def create_forum_discussion(
    forumid: int,
    subject: str,
    message: str,
    dry_run: bool = True,
    reason: str | None = None,
) -> ForumPost:
    """Preview or start a new forum discussion.

    Use dry_run=True to inspect the intended discussion without changing Moodle. Use dry_run=False only after the user explicitly confirms the post and provides reason.

    Args:
        forumid: The forum ID.
        subject: The discussion subject.
        message: The discussion content (HTML).
        dry_run: If True, return a preview and do not write to Moodle.
        reason: Human-readable reason required when dry_run is False.
    Returns:
        Discussion id and timestamp.
    """
    try:
        return await api.create_forum_discussion(forumid, subject, message, dry_run, reason)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


async def get_announcements(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[AnnouncementPost]:
    """List course announcements from news-type forums.

    Args:
        course_ids: Optional list of course IDs to filter by.
        limit: Maximum announcements to return, capped server-side.
    Returns:
        Announcements with subject, message, author, timemodified.
    """
    return await api.get_announcements(course_ids, limit)
