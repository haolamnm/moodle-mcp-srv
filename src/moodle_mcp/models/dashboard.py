"""Dashboard Summary response models."""

from __future__ import annotations

from pydantic import BaseModel

from moodle_mcp.models.calendar import Deadline  # noqa: TC001


class DashboardGrade(BaseModel):
    name: str
    course: str
    grade: float


class RecentActivity(BaseModel):
    name: str
    course: str | None
    timemodified: int | None


class DashboardSummary(BaseModel):
    overdue: list[Deadline]
    due_today: list[Deadline]
    due_this_week: list[Deadline]
    new_grades: list[DashboardGrade]
    recent_activity: list[RecentActivity]
    total_pending: int
