"""MCP surface inspection CLI commands."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated

import typer

from moodle_mcp.server import create_server


def inspect_server(
    json_output: Annotated[
        bool,
        typer.Option(
            "--json", help="Print tools, resources, resource templates, and prompts as JSON."
        ),
    ] = False,
) -> None:
    """Print the MCP tools, resources, resource templates, and prompts registered locally."""
    summary = asyncio.run(_server_summary())
    if json_output:
        typer.echo(json.dumps(summary, sort_keys=True))
        return

    for section, names in summary.items():
        typer.echo(f"{section}:")
        for name in names:
            typer.echo(f"- {name}")


async def _server_summary() -> dict[str, list[str]]:
    server = create_server()
    tools = await server.list_tools()
    resources = await server.list_resources()
    templates = await server.list_resource_templates()
    prompts = await server.list_prompts()
    return {
        "tools": sorted(tool.name for tool in tools),
        "resources": sorted(str(resource.uri) for resource in resources),
        "resource_templates": sorted(template.uri_template for template in templates),
        "prompts": sorted(prompt.name for prompt in prompts),
    }
