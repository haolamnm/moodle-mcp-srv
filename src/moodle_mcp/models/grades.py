"""Grade response models."""

from __future__ import annotations

from pydantic import BaseModel


class GradeItem(BaseModel):
    id: int
    name: str
    coursename: str | None
    courseid: int | None
    grade_raw: float | None
    grade_percent: str | None
    grade_letter: str | None
    range_min: float | None
    range_max: float | None
    feedback: str | None


class CompletionActivity(BaseModel):
    id: int
    name: str
    modname: str
    completionstatus: str
    timecompleted: int | None
