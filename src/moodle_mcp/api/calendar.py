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
    require_write_reason,
)
from moodle_mcp.api.coercion import (
    as_int,
    as_object,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import CalendarEvent, Deadline, WriteReceipt
from moodle_mcp.moodle import (
    APIFunction,
    MoodleAPIError,
    format_array_params,
    get_moodle_api_data,
)

if TYPE_CHECKING:
    from moodle_mcp.models import JsonObject, MoodleResponse


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
    """Return a merged, time-sorted list of upcoming deadlines.

    Assignment and quiz deadlines degrade independently: if one source's Moodle
    Web Service Function Name is unavailable or refused, its deadlines are skipped
    rather than failing the whole list.
    """
    courses = await get_enrolled_courses()
    course_ids = [course_id(course) for course in courses if course_id(course) > 0]
    if not course_ids:
        return []

    course_map = {course_id(course): course_name(course) for course in courses}
    deadlines: list[Deadline] = []
    for source in (_assignment_deadlines(course_ids), _quiz_deadlines(course_ids, course_map)):
        try:
            deadlines.extend(await source)
        except MoodleAPIError:
            continue

    deadlines.sort(key=lambda deadline: deadline.duedate)
    current = now_ts()
    cutoff = current + daysahead * DAYS_SECONDS
    upcoming = [deadline for deadline in deadlines if current <= deadline.duedate <= cutoff]
    return limit_items(upcoming, limit)


async def create_calendar_event(
    name: str,
    timestart: int,
    description: str | None = None,
    dry_run: bool = True,
    reason: str | None = None,
) -> WriteReceipt:
    """Create a personal (user) Calendar Event."""
    if dry_run:
        return WriteReceipt(
            dry_run=True,
            action="create_calendar_event",
            target_type="calendar_event",
            target_id=name,
            would_change=["Create a personal Moodle calendar event."],
            warnings=["Dry run only. Pass dry_run=False with a reason to create this event."],
            moodle_function=APIFunction.core_calendar_create_calendar_events.value,
        )

    require_write_reason(reason)
    params: dict[str, str] = {
        "events[0][name]": name,
        "events[0][timestart]": str(timestart),
        "events[0][eventtype]": "user",
    }
    if description is not None:
        params["events[0][description]"] = description

    data = await get_moodle_api_data(APIFunction.core_calendar_create_calendar_events, params)
    event_id = _first_event_id(data)
    return WriteReceipt(
        dry_run=False,
        action="create_calendar_event",
        target_type="calendar_event",
        target_id=event_id if event_id is not None else name,
        reason=reason,
        changed=(
            [f"Created calendar event {event_id}."]
            if event_id is not None
            else ["Moodle accepted the calendar event request."]
        ),
        moodle_function=APIFunction.core_calendar_create_calendar_events.value,
    )


def _first_event_id(data: MoodleResponse) -> int | None:
    if not isinstance(data, dict):
        return None
    events = object_list(data.get("events"))
    if not events:
        return None
    return as_optional_int(events[0].get("id"))


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
