from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import grades
from moodle_mcp.moodle import APIFunction

if TYPE_CHECKING:
    import pytest


def test_get_grades_formats_grade_items(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[APIFunction, dict[str, str] | None]] = []

    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [10]

    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_enrolled_courses(userid: int | None = None) -> list[dict[str, object]]:
        await asyncio.sleep(0)
        assert userid is None
        return [{"id": 10, "fullname": "Algorithms"}]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        calls.append((function, params))
        return {
            "gradeitems": [
                {
                    "id": "7",
                    "itemname": "Assignment 1",
                    "graderaw": "8.5",
                    "percentageformatted": "85%",
                    "lettergradeformatted": "A",
                    "rangemin": "0",
                    "rangemax": "10",
                    "feedback": {"text": "Good"},
                }
            ]
        }

    monkeypatch.setattr(grades, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(grades, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(grades, "get_enrolled_courses", fake_get_enrolled_courses)
    monkeypatch.setattr(grades, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(grades.get_grades([10]))

    assert calls == [
        (
            APIFunction.gradereport_user_get_grade_items,
            {"courseid": "10", "userid": "42"},
        )
    ]
    assert [item.model_dump() for item in result] == [
        {
            "id": 7,
            "name": "Assignment 1",
            "coursename": "Algorithms",
            "courseid": 10,
            "grade_raw": 8.5,
            "grade_percent": "85%",
            "grade_letter": "A",
            "range_min": 0.0,
            "range_max": 10.0,
            "feedback": "Good",
        }
    ]


def test_get_grades_returns_empty_without_courses(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        _ = course_ids
        return []

    monkeypatch.setattr(grades, "get_course_ids", fake_get_course_ids)

    assert asyncio.run(grades.get_grades()) == []


def test_get_course_progress_formats_completion_status(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.core_completion_get_activities_completion_status
        assert params == {"courseid": "10", "userid": "42"}
        return {
            "statuses": [
                {
                    "cmid": "1",
                    "activityname": "Lecture",
                    "modname": "resource",
                    "state": "1",
                    "timecompleted": "123",
                },
                {
                    "cmid": "2",
                    "activityname": "Quiz",
                    "modname": "quiz",
                    "state": "0",
                },
            ]
        }

    monkeypatch.setattr(grades, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(grades, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(grades.get_course_progress(10))

    assert [activity.model_dump() for activity in result] == [
        {
            "id": 1,
            "name": "Lecture",
            "modname": "resource",
            "completionstatus": "complete",
            "timecompleted": 123,
        },
        {
            "id": 2,
            "name": "Quiz",
            "modname": "quiz",
            "completionstatus": "incomplete",
            "timecompleted": None,
        },
    ]


def test_get_course_progress_returns_empty_for_unexpected_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        _ = function, params
        return []

    monkeypatch.setattr(grades, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(grades, "get_moodle_api_data", fake_get_moodle_api_data)

    assert asyncio.run(grades.get_course_progress(10)) == []


def test_mark_activity_complete_defaults_to_dry_run() -> None:
    receipt = asyncio.run(grades.mark_activity_complete(5))

    assert receipt.dry_run is True
    assert receipt.action == "mark_activity_complete"
    assert receipt.target_id == 5
    assert receipt.would_change == ["Mark this activity complete."]


def test_mark_activity_complete_calls_moodle_when_confirmed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        assert function == (APIFunction.core_completion_update_activity_completion_status_manually)
        captured.update(params or {})
        return []

    monkeypatch.setattr(grades, "get_moodle_api_data", fake_get_moodle_api_data)

    receipt = asyncio.run(
        grades.mark_activity_complete(5, completed=False, dry_run=False, reason="User confirmed")
    )

    assert captured == {"cmid": "5", "completed": "0"}
    assert receipt.changed == ["Marked activity 5 incomplete."]
