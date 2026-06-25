"""Shared helpers for Moodle API tool modules."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from moodle_mcp.api.coercion import as_int, as_optional_int, object_list
from moodle_mcp.moodle import APIFunction, get_moodle_api_data, resolve_current_user_id

if TYPE_CHECKING:
    from moodle_mcp.models import JsonObject

DAYS_SECONDS = 86_400
DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def now_ts() -> int:
    """Current Unix timestamp."""
    return int(datetime.now(UTC).timestamp())


async def get_enrolled_courses(userid: int | None = None) -> list[JsonObject]:
    """Fetch all courses the current user is enrolled in."""
    uid = userid or await resolve_current_user_id()
    data = await get_moodle_api_data(
        APIFunction.core_enrol_get_users_courses,
        {"userid": str(uid)},
    )
    return object_list(data)


async def get_course_ids(course_ids: list[int] | None = None) -> list[int]:
    """Resolve course IDs, defaulting to all enrolled courses."""
    if course_ids:
        return course_ids

    courses = await get_enrolled_courses()
    ids: list[int] = []
    for course in courses:
        course_id = as_optional_int(course.get("id"))
        if course_id is not None:
            ids.append(course_id)
    return ids


def days_remaining(timestamp: int, now: int | None = None) -> int:
    """Return whole days remaining from now to the timestamp."""
    current = now_ts() if now is None else now
    return max(0, (timestamp - current) // DAYS_SECONDS)


def normalize_limit(limit: int, *, default: int = DEFAULT_LIMIT, maximum: int = MAX_LIMIT) -> int:
    """Clamp list limits to a small positive range."""
    if limit <= 0:
        return default
    return min(limit, maximum)


def limit_items[T](items: list[T], limit: int, *, maximum: int = MAX_LIMIT) -> list[T]:
    """Return at most limit items."""
    return items[: normalize_limit(limit, maximum=maximum)]


def course_name(course: JsonObject) -> str:
    """Return a course fullname from raw Moodle course data."""
    fullname = course.get("fullname")
    return fullname if isinstance(fullname, str) else ""


def course_id(course: JsonObject) -> int:
    """Return a course ID from raw Moodle course data."""
    return as_int(course.get("id"))
