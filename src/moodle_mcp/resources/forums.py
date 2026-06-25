"""Forum MCP resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from moodle_mcp import api

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register forum-facing resources."""
    mcp.resource(
        "moodle://forums/{courseid}/digest",
        name="forum_digest_resource",
        description="Read-only forum discussion digest for an enrolled Moodle course.",
        mime_type="application/json",
    )(forum_digest_resource)


async def forum_digest_resource(courseid: int) -> str:
    """Return course forum discussions as compact JSON resource text."""
    discussions = await api.get_forum_discussions(courseid)
    return TypeAdapter(list[api.ForumDiscussion]).dump_json(discussions).decode()
