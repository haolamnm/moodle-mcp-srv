"""Forum and Announcement response models."""

from __future__ import annotations

from pydantic import BaseModel

from moodle_mcp.models.strings import MoodleHtml, MoodleText  # noqa: TC001


class ForumDiscussion(BaseModel):
    id: int
    name: MoodleText
    author: MoodleText | None
    timemodified: int
    postcount: int | None
    pinned: bool | None


class ForumPost(BaseModel):
    id: int
    timemodified: int
    dry_run: bool = False
    message: MoodleText | None = None


class AnnouncementPost(BaseModel):
    id: int
    subject: MoodleText
    message: MoodleHtml | None
    author: MoodleText | None
    timemodified: int
    courseid: int
    coursename: MoodleText | None
