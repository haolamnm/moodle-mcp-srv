"""Current Moodle user resolution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from moodle_mcp.moodle.client import get_moodle_api_data
from moodle_mcp.moodle.errors import MoodleAPIError
from moodle_mcp.moodle.functions import APIFunction

if TYPE_CHECKING:
    from moodle_mcp.models import JsonValue


@dataclass(slots=True)
class _UserIdCache:
    user_id: int | None = None


_user_id_cache = _UserIdCache()


def reset_current_user_cache() -> None:
    """Clear the cached current Moodle user ID."""
    _user_id_cache.user_id = None


async def resolve_current_user_id() -> int:
    """Resolve the current Moodle user ID from the API token."""
    if _user_id_cache.user_id is not None:
        return _user_id_cache.user_id

    data = await get_moodle_api_data(APIFunction.core_webservice_get_site_info)
    if not isinstance(data, dict) or "userid" not in data:
        raise MoodleAPIError(
            "no_userid",
            "Could not resolve user ID from token",
            "core_webservice_get_site_info",
        )

    user_id = _int_value(data["userid"])
    if user_id is None:
        raise MoodleAPIError(
            "invalid_userid",
            "Moodle returned a non-numeric user ID",
            "core_webservice_get_site_info",
        )

    _user_id_cache.user_id = user_id
    return user_id


def _int_value(value: JsonValue | None) -> int | None:
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
