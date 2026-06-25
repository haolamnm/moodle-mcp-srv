"""Calendar Event and deadline response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from moodle_mcp.models.strings import MoodleIsoDateTimeText, MoodleText  # noqa: TC001


class CalendarEvent(BaseModel):
    id: int
    name: MoodleText
    description: MoodleText | None
    timestart: int
    timestart_iso: MoodleIsoDateTimeText
    eventtype: MoodleText
    courseid: int | None
    coursename: MoodleText | None


class Deadline(BaseModel):
    type: Literal["assignment", "quiz"]
    id: int
    name: MoodleText
    course: MoodleText
    duedate: int
    daysremaining: int
