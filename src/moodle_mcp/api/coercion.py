"""Small coercion helpers for Moodle's JSON responses."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from moodle_mcp.models import JsonArray, JsonObject, JsonValue


def as_object(value: JsonValue | None) -> JsonObject:
    """Return a JSON object or an empty object for non-object values."""
    if isinstance(value, dict):
        return value
    return {}


def object_list(value: JsonValue | None) -> list[JsonObject]:
    """Return only object items from a JSON array."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def as_array(value: JsonValue | None) -> JsonArray:
    """Return a JSON array or an empty array for non-array values."""
    if isinstance(value, list):
        return value
    return []


def as_str(value: JsonValue | None, default: str = "") -> str:
    """Return a string value or the default."""
    return value if isinstance(value, str) else default


def as_optional_str(value: JsonValue | None) -> str | None:
    """Return a string value or None."""
    return value if isinstance(value, str) else None


def as_int(value: JsonValue | None, default: int = 0) -> int:
    """Return an integer value or the default."""
    parsed = as_optional_int(value)
    return default if parsed is None else parsed


def as_optional_int(value: JsonValue | None) -> int | None:
    """Return an integer value when Moodle sends one as int, float, or string."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def as_optional_float(value: JsonValue | None) -> float | None:
    """Return a float value when Moodle sends one as number or string."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def as_bool(value: JsonValue | None, default: bool = False) -> bool:
    """Return a bool value when Moodle sends one as bool, number, or string."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return value != 0
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes"}
    return default
