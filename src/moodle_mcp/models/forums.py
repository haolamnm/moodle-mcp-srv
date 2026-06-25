"""Forum and Announcement response models."""

from __future__ import annotations

from pydantic import BaseModel


class ForumDiscussion(BaseModel):
    id: int
    name: str
    author: str | None
    timemodified: int
    postcount: int | None
    pinned: bool | None


class ForumPost(BaseModel):
    id: int
    timemodified: int
    dry_run: bool = False
    message: str | None = None


class AnnouncementPost(BaseModel):
    id: int
    subject: str
    message: str | None
    author: str | None
    timemodified: int
    courseid: int
    coursename: str | None
