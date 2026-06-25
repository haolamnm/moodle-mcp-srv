"""Forum and Announcement tool implementations."""

from __future__ import annotations

from moodle_mcp.api._helpers import get_course_ids, limit_items
from moodle_mcp.api.coercion import (
    as_bool,
    as_int,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import AnnouncementPost, ForumDiscussion, ForumPost, JsonObject
from moodle_mcp.moodle import APIFunction, format_array_params, get_moodle_api_data


async def get_forum_discussions(
    courseid: int,
    forumid: int | None = None,
    limit: int = 50,
) -> list[ForumDiscussion]:
    """Return discussions for forums in a course."""
    forums = await _get_course_forums(courseid)
    target_forums = [
        forum for forum in forums if forumid is None or as_int(forum.get("id")) == forumid
    ]

    discussions: list[ForumDiscussion] = []
    for forum in target_forums:
        data = await get_moodle_api_data(
            APIFunction.mod_forum_get_forum_discussions,
            {"forumid": str(as_int(forum.get("id")))},
        )
        if not isinstance(data, dict):
            continue

        for discussion in object_list(data.get("discussions")):
            discussions.append(_format_discussion(discussion))
    return limit_items(discussions, limit)


async def post_forum_reply(
    discussionid: int,
    message: str,
    subject: str | None = None,
    dry_run: bool = True,
    reason: str | None = None,
) -> ForumPost:
    """Post a reply to a discussion thread."""
    if dry_run:
        return ForumPost(
            id=0,
            timemodified=0,
            dry_run=True,
            message="Dry run only. Pass dry_run=False with a reason to post this reply.",
        )

    _require_write_reason(reason)
    params: dict[str, str] = {
        "discussionid": str(discussionid),
        "postsubject": subject or "Re: Discussion",
        "message": message,
        "messageformat": "1",
    }
    data = await get_moodle_api_data(APIFunction.mod_forum_add_discussion_post, params)
    if isinstance(data, dict):
        return ForumPost(
            id=as_int(data.get("postid")),
            timemodified=as_int(data.get("timemodified")),
        )
    return ForumPost(id=0, timemodified=0)


async def create_forum_discussion(
    forumid: int,
    subject: str,
    message: str,
    dry_run: bool = True,
    reason: str | None = None,
) -> ForumPost:
    """Start a new discussion thread in a forum."""
    if dry_run:
        return ForumPost(
            id=0,
            timemodified=0,
            dry_run=True,
            message="Dry run only. Pass dry_run=False with a reason to create this discussion.",
        )

    _require_write_reason(reason)
    params: dict[str, str] = {
        "forumid": str(forumid),
        "subject": subject,
        "message": message,
        "messageformat": "1",
    }
    data = await get_moodle_api_data(APIFunction.mod_forum_add_discussion, params)
    if isinstance(data, dict):
        return ForumPost(
            id=as_int(data.get("discussionid")),
            timemodified=as_int(data.get("timemodified")),
        )
    return ForumPost(id=0, timemodified=0)


async def get_announcements(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[AnnouncementPost]:
    """Return announcement posts from news-type forums."""
    cids = await get_course_ids(course_ids)
    if not cids:
        return []

    announcements: list[AnnouncementPost] = []
    for cid in cids:
        news_forums = [
            forum for forum in await _get_course_forums(cid) if as_str(forum.get("type")) == "news"
        ]
        for forum in news_forums:
            announcements.extend(await _get_forum_announcements(cid, forum))
    return limit_items(announcements, limit)


async def _get_course_forums(courseid: int) -> list[JsonObject]:
    data = await get_moodle_api_data(
        APIFunction.mod_forum_get_forums_by_courses,
        format_array_params("courseids", [courseid]),
    )
    if not isinstance(data, list):
        return []
    return object_list(data)


async def _get_forum_announcements(courseid: int, forum: JsonObject) -> list[AnnouncementPost]:
    data = await get_moodle_api_data(
        APIFunction.mod_forum_get_forum_discussions,
        {"forumid": str(as_int(forum.get("id")))},
    )
    if not isinstance(data, dict):
        return []

    announcements: list[AnnouncementPost] = []
    for discussion in object_list(data.get("discussions")):
        announcements.append(
            AnnouncementPost(
                id=as_int(discussion.get("id")),
                subject=as_str(discussion.get("name")),
                message=as_optional_str(discussion.get("message")),
                author=as_optional_str(discussion.get("userfullname"))
                or as_optional_str(discussion.get("author")),
                timemodified=as_int(discussion.get("timemodified")),
                courseid=courseid,
                coursename=as_optional_str(forum.get("name")),
            )
        )
    return announcements


def _format_discussion(discussion: JsonObject) -> ForumDiscussion:
    postcount = as_optional_int(discussion.get("postcount"))
    if postcount is None:
        postcount = as_optional_int(discussion.get("numreplies"))

    return ForumDiscussion(
        id=as_int(discussion.get("id")),
        name=as_str(discussion.get("name")),
        author=as_optional_str(discussion.get("userfullname"))
        or as_optional_str(discussion.get("author")),
        timemodified=as_int(discussion.get("timemodified")),
        postcount=postcount,
        pinned=as_bool(discussion.get("pinned")),
    )


def _require_write_reason(reason: str | None) -> None:
    if reason is None or not reason.strip():
        raise ValueError("Write tools require a human-readable reason when dry_run is false.")
