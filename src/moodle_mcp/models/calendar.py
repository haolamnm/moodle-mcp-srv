"""Calendar Event and deadline response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class CalendarEvent(BaseModel):
    id: int
    name: str
    description: str | None
    timestart: int
    timestart_iso: str
    eventtype: str
    courseid: int | None
    coursename: str | None


class Deadline(BaseModel):
    type: Literal["assignment", "quiz"]
    id: int
    name: str
    course: str
    duedate: int
    daysremaining: int
