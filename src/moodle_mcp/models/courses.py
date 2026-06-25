"""Course response models."""

from __future__ import annotations

from pydantic import BaseModel


class SiteInfo(BaseModel):
    sitename: str
    siteurl: str | None
    userid: int
    username: str | None
    firstname: str | None
    lastname: str | None
    fullname: str | None
    release: str | None
    version: str | None


class Course(BaseModel):
    id: int
    fullname: str
    shortname: str
    category: int
    summary: str
    startdate: int | None
    enddate: int | None
    progress: float | None


class Module(BaseModel):
    id: int
    name: str
    modname: str
    url: str | None
    description: str | None


class CourseSection(BaseModel):
    id: int
    name: str
    summary: str | None
    modules: list[Module]
