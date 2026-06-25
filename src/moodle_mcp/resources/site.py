"""Site-level MCP resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp import api

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register site-level resources."""
    mcp.resource(
        "moodle://site/profile",
        name="site_profile_resource",
        description="Read-only Site Info for the configured Moodle token.",
        mime_type="application/json",
    )(site_profile_resource)
    mcp.resource(
        "moodle://site/features",
        name="site_features_resource",
        description="Read-only Moodle Feature availability report.",
        mime_type="application/json",
    )(site_features_resource)


async def site_profile_resource() -> str:
    """Return Site Info as compact JSON resource text."""
    return (await api.get_site_info()).model_dump_json()


async def site_features_resource() -> str:
    """Return Moodle Feature availability as compact JSON resource text."""
    return (await api.get_server_capabilities()).model_dump_json()
