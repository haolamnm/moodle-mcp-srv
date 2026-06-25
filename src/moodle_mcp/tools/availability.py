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
    """Raise a friendly ToolError, separating setup gaps from Access Errors."""
    kind = api.classify_failure(exc.error_code)
    if kind is api.FailureKind.missing_function:
        raise ToolError(
            api.feature_unavailable_message(
                feature,
                api.required_function_names(feature),
            )
        ) from exc
    if kind is api.FailureKind.access_denied:
        raise ToolError(api.access_error_message(feature, exc.error_code)) from exc
    raise ToolError(str(exc)) from exc
