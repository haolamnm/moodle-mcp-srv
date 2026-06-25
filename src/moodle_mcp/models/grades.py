"""Grade response models."""

from __future__ import annotations

from pydantic import BaseModel

from moodle_mcp.models.strings import MoodleText  # noqa: TC001


class GradeItem(BaseModel):
    id: int
    name: MoodleText
    coursename: MoodleText | None
    courseid: int | None
    grade_raw: float | None
    grade_percent: MoodleText | None
    grade_letter: MoodleText | None
    range_min: float | None
    range_max: float | None
    feedback: MoodleText | None


class CompletionActivity(BaseModel):
    id: int
    name: MoodleText
    modname: MoodleText
    completionstatus: str
    timecompleted: int | None
