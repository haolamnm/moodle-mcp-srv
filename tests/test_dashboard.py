from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import dashboard
from moodle_mcp.models import Assignment, Course
from moodle_mcp.moodle import MoodleAPIError

if TYPE_CHECKING:
    import pytest


def test_dashboard_summary_tolerates_grade_report_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current = 1_000_000

    async def fake_get_my_courses() -> list[Course]:
        await asyncio.sleep(0)
        return [
            Course(
                id=10,
                fullname="Course",
                shortname="C",
                category=1,
                summary="",
                startdate=None,
                enddate=None,
                progress=None,
            )
        ]

    async def fake_get_assignments(course_ids: list[int]) -> list[Assignment]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [
            Assignment(
                id=99,
                cmid=1,
                course=10,
                name="Due Soon",
                duedate=current + 60,
                cutoffdate=None,
                allowsubmissionsfromdate=None,
                grade=None,
                timemodified=None,
                intro=None,
                introformat=1,
                coursemodule=None,
            )
        ]

    async def fake_get_grades(course_ids: list[int]) -> object:
        await asyncio.sleep(0)
        assert course_ids == [10]
        raise MoodleAPIError("invalidresponse", "Invalid response value detected", "grades")

    monkeypatch.setattr(dashboard, "now_ts", lambda: current)
    monkeypatch.setattr(dashboard, "get_my_courses", fake_get_my_courses)
    monkeypatch.setattr(dashboard, "get_assignments", fake_get_assignments)
    monkeypatch.setattr(dashboard, "get_grades", fake_get_grades)

    summary = asyncio.run(dashboard.dashboard_summary())

    assert summary.new_grades == []
    assert [deadline.name for deadline in summary.due_today] == ["Due Soon"]
    assert any("grades" in warning for warning in summary.warnings)


def test_dashboard_summary_degrades_when_assignments_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_my_courses() -> list[Course]:
        await asyncio.sleep(0)
        return [
            Course(
                id=10,
                fullname="Course",
                shortname="C",
                category=1,
                summary="",
                startdate=None,
                enddate=None,
                progress=None,
            )
        ]

    async def fake_get_assignments(course_ids: list[int]) -> object:
        await asyncio.sleep(0)
        raise MoodleAPIError("invalidrecord", "Function not found", "assignments")

    async def fake_get_grades(course_ids: list[int]) -> list[object]:
        await asyncio.sleep(0)
        return []

    monkeypatch.setattr(dashboard, "now_ts", lambda: 1_000_000)
    monkeypatch.setattr(dashboard, "get_my_courses", fake_get_my_courses)
    monkeypatch.setattr(dashboard, "get_assignments", fake_get_assignments)
    monkeypatch.setattr(dashboard, "get_grades", fake_get_grades)

    summary = asyncio.run(dashboard.dashboard_summary())

    assert summary.total_pending == 0
    assert summary.due_today == []
    assert any("assignments" in warning for warning in summary.warnings)


def test_dashboard_summary_degrades_when_courses_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_my_courses() -> list[Course]:
        await asyncio.sleep(0)
        raise MoodleAPIError("accessexception", "Access denied", "courses")

    monkeypatch.setattr(dashboard, "get_my_courses", fake_get_my_courses)

    summary = asyncio.run(dashboard.dashboard_summary())

    assert summary.total_pending == 0
    assert summary.warnings == ["Skipped courses: Moodle returned [accessexception]."]
