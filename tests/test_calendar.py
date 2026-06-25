from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Protocol

from moodle_mcp.api import calendar
from moodle_mcp.moodle import APIFunction

if TYPE_CHECKING:
    import pytest


class TimeMachineFixture(Protocol):
    def move_to(self, destination: object, *, tick: bool = True) -> None: ...


DAYS_SECONDS = 86_400


def test_now_ts_is_deterministic_with_time_machine(
    time_machine: TimeMachineFixture,
) -> None:
    frozen = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    time_machine.move_to(frozen, tick=False)

    assert calendar.now_ts() == int(frozen.timestamp())


def test_get_calendar_events_filters_by_daysahead(monkeypatch: pytest.MonkeyPatch) -> None:
    current = 1_000_000
    monkeypatch.setattr(calendar, "now_ts", lambda: current)

    async def fake_get_moodle_api_data(
        function: object,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        _ = function, params
        return {
            "events": [
                {"id": 1, "name": "Past", "timestart": current - 1, "eventtype": "course"},
                {
                    "id": 2,
                    "name": "Soon",
                    "timestart": current + DAYS_SECONDS,
                    "eventtype": "course",
                },
                {
                    "id": 3,
                    "name": "Late",
                    "timestart": current + 3 * DAYS_SECONDS,
                    "eventtype": "course",
                },
            ]
        }

    monkeypatch.setattr(calendar, "get_moodle_api_data", fake_get_moodle_api_data)

    events = asyncio.run(calendar.get_calendar_events(daysahead=2))

    assert [event.id for event in events] == [2]


def test_get_upcoming_deadlines_excludes_overdue_and_sets_quiz_course(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current = 1_000_000
    monkeypatch.setattr(calendar, "now_ts", lambda: current)

    async def fake_get_enrolled_courses() -> list[dict[str, object]]:
        await asyncio.sleep(0)
        return [{"id": 10, "fullname": "Algorithms"}]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        _ = params
        if function == APIFunction.mod_assign_get_assignments:
            return {
                "courses": [
                    {
                        "id": 10,
                        "fullname": "Algorithms",
                        "assignments": [
                            {"id": 1, "name": "Old Assignment", "duedate": current - 1},
                            {"id": 2, "name": "New Assignment", "duedate": current + 100},
                        ],
                    }
                ]
            }
        return {
            "quizzes": [
                {
                    "id": 3,
                    "name": "Quiz 1",
                    "course": 10,
                    "timeclose": current + 200,
                }
            ]
        }

    monkeypatch.setattr(calendar, "get_enrolled_courses", fake_get_enrolled_courses)
    monkeypatch.setattr(calendar, "get_moodle_api_data", fake_get_moodle_api_data)

    deadlines = asyncio.run(calendar.get_upcoming_deadlines(daysahead=1))

    assert [deadline.name for deadline in deadlines] == ["New Assignment", "Quiz 1"]
    assert [deadline.course for deadline in deadlines] == ["Algorithms", "Algorithms"]


def test_create_calendar_event_defaults_to_dry_run() -> None:
    receipt = asyncio.run(calendar.create_calendar_event("Study", 1_000_000))

    assert receipt.dry_run is True
    assert receipt.action == "create_calendar_event"
    assert receipt.target_id == "Study"
    assert receipt.moodle_function == APIFunction.core_calendar_create_calendar_events.value


def test_create_calendar_event_calls_moodle_when_confirmed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.core_calendar_create_calendar_events
        captured.update(params or {})
        return {"events": [{"id": 7}]}

    monkeypatch.setattr(calendar, "get_moodle_api_data", fake_get_moodle_api_data)

    receipt = asyncio.run(
        calendar.create_calendar_event(
            "Study", 1_000_000, "Chapter 4", dry_run=False, reason="User confirmed"
        )
    )

    assert captured == {
        "events[0][name]": "Study",
        "events[0][timestart]": "1000000",
        "events[0][eventtype]": "user",
        "events[0][description]": "Chapter 4",
    }
    assert receipt.changed == ["Created calendar event 7."]
    assert receipt.target_id == 7
