"""Course response models."""

from __future__ import annotations

from pydantic import BaseModel

from moodle_mcp.models.strings import (  # noqa: TC001
    CourseShortName,
    MoodleHtml,
    MoodleModuleName,
    MoodleText,
    MoodleUrlString,
    MoodleUsername,
)


class SiteInfo(BaseModel):
    sitename: MoodleText
    siteurl: MoodleUrlString | None
    userid: int
    username: MoodleUsername | None
    firstname: MoodleText | None
    lastname: MoodleText | None
    fullname: MoodleText | None
    release: str | None
    version: str | None


class Course(BaseModel):
    id: int
    fullname: MoodleText
    shortname: CourseShortName
    category: int
    summary: MoodleHtml
    startdate: int | None
    enddate: int | None
    progress: float | None


class Module(BaseModel):
    id: int
    name: MoodleText
    modname: MoodleModuleName
    url: MoodleUrlString | None
    description: MoodleHtml | None


class CourseSection(BaseModel):
    id: int
    name: MoodleText
    summary: MoodleHtml | None
    modules: list[Module]
