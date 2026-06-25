"""Tool Wrapper availability helpers."""

from __future__ import annotations

from typing import Never

from fastmcp.exceptions import ToolError

from moodle_mcp import api


async def require_feature(feature: api.MoodleFeature) -> None:
    """Convert Moodle Feature availability errors into ToolError."""
    try:
        await api.ensure_feature_available(feature)
    except api.UnavailableFeatureError as exc:
        raise ToolError(str(exc)) from exc


def raise_tool_error_for_moodle_failure(
    exc: api.MoodleAPIError,
    feature: api.MoodleFeature,
) -> Never:
    """Raise a friendly ToolError for known Moodle Feature setup failures."""
    if exc.error_code in {"invalidrecord", "accessexception"}:
        raise ToolError(
            api.feature_unavailable_message(
                feature,
                api.required_function_names(feature),
            )
        ) from exc
    raise ToolError(str(exc)) from exc
