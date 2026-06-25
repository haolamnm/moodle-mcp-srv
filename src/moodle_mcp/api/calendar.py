"""Calendar Event and deadline tool implementations."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from moodle_mcp.api._helpers import (
    DAYS_SECONDS,
    course_id,
    course_name,
    days_remaining,
    get_enrolled_courses,
    limit_items,
    now_ts,
)
from moodle_mcp.api.coercion import (
    as_int,
    as_object,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import CalendarEvent, Deadline
from moodle_mcp.moodle import APIFunction, format_array_params, get_moodle_api_data

if TYPE_CHECKING:
    from moodle_mcp.models import JsonObject


async def get_calendar_events(daysahead: int = 14, limit: int = 50) -> list[CalendarEvent]:
    """Return upcoming calendar events."""
    data = await get_moodle_api_data(
        APIFunction.core_calendar_get_calendar_upcoming_view,
    )
    if not isinstance(data, dict):
        return []
    current = now_ts()
    cutoff = current + daysahead * DAYS_SECONDS
    events = [
        event
        for event in _format_events(object_list(data.get("events")))
        if current <= event.timestart <= cutoff
    ]
    return limit_items(events, limit)


async def get_upcoming_deadlines(daysahead: int = 7, limit: int = 50) -> list[Deadline]:
    """Return a merged, time-sorted list of upcoming deadlines."""
    courses = await get_enrolled_courses()
    course_ids = [course_id(course) for course in courses if course_id(course) > 0]
    if not course_ids:
        return []

    deadlines = await _assignment_deadlines(course_ids)
    course_map = {course_id(course): course_name(course) for course in courses}
    deadlines.extend(await _quiz_deadlines(course_ids, course_map))

    deadlines.sort(key=lambda deadline: deadline.duedate)
    current = now_ts()
    cutoff = current + daysahead * DAYS_SECONDS
    upcoming = [deadline for deadline in deadlines if current <= deadline.duedate <= cutoff]
    return limit_items(upcoming, limit)


def _format_events(events_raw: list[JsonObject]) -> list[CalendarEvent]:
    result: list[CalendarEvent] = []
    for event in events_raw:
        course = as_object(event.get("course"))
        timestart = as_int(event.get("timestart"))
        result.append(
            CalendarEvent(
                id=as_int(event.get("id")),
                name=as_str(event.get("name")),
                description=as_optional_str(event.get("description")),
                timestart=timestart,
                timestart_iso=(
                    datetime.fromtimestamp(timestart, tz=UTC).isoformat() if timestart else ""
                ),
                eventtype=as_str(event.get("eventtype")),
                courseid=as_optional_int(course.get("id")),
                coursename=as_optional_str(course.get("fullname")),
            )
        )
    return result


async def _assignment_deadlines(course_ids: list[int]) -> list[Deadline]:
    data = await get_moodle_api_data(
        APIFunction.mod_assign_get_assignments,
        format_array_params("courseids", course_ids),
    )
    if not isinstance(data, dict):
        return []

    deadlines: list[Deadline] = []
    current = now_ts()
    for course in object_list(data.get("courses")):
        for assignment in object_list(course.get("assignments")):
            due = as_optional_int(assignment.get("duedate"))
            if due is None or due <= 0:
                continue
            deadlines.append(
                Deadline(
                    type="assignment",
                    id=as_int(assignment.get("id")),
                    name=as_str(assignment.get("name")),
                    course=as_str(course.get("fullname")),
                    duedate=due,
                    daysremaining=days_remaining(due, current),
                )
            )
    return deadlines


async def _quiz_deadlines(
    course_ids: list[int],
    course_map: dict[int, str],
) -> list[Deadline]:
    data = await get_moodle_api_data(
        APIFunction.mod_quiz_get_quizzes_by_courses,
        format_array_params("courseids", course_ids),
    )
    if not isinstance(data, dict):
        return []

    deadlines: list[Deadline] = []
    current = now_ts()
    for quiz in object_list(data.get("quizzes")):
        close = as_optional_int(quiz.get("timeclose"))
        if close is None or close <= 0:
            continue
        deadlines.append(
            Deadline(
                type="quiz",
                id=as_int(quiz.get("id")),
                name=as_str(quiz.get("name")),
                course=course_map.get(as_int(quiz.get("course")), ""),
                duedate=close,
                daysremaining=days_remaining(close, current),
            )
        )
    return deadlines
