"""FastMCP server composition root."""

from __future__ import annotations

from fastmcp import FastMCP

from moodle_mcp.prompts import register_prompts
from moodle_mcp.resources import register_resources
from moodle_mcp.tools import register_tools


def create_server() -> FastMCP:
    """Create a fully registered Moodle MCP server."""
    server = FastMCP(
        "Moodle MCP",
        instructions=(
            "Your Moodle dashboard, available to AI. "
            "All tools are cross-course by default -- pass course_ids to filter. "
            "Read-only context is available through moodle:// resources. "
            "Write tools default to dry_run=True and require reason when dry_run is false. "
            "The current user is resolved from the MOODLE_API_TOKEN."
        ),
    )
    register_tools(server)
    register_resources(server)
    register_prompts(server)
    return server


mcp = create_server()


def main() -> None:
    """Run the MCP server over stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
