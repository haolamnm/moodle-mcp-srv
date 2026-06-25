"""MCP server CLI commands."""

from __future__ import annotations

from typing import Annotated

import typer

from moodle_mcp.server import create_server


def serve(
    http: Annotated[
        bool,
        typer.Option("--http", help="Run over HTTP transport instead of stdio."),
    ] = False,
    host: Annotated[
        str,
        typer.Option("--host", help="Host for HTTP transport."),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option("--port", min=1, max=65535, help="Port for HTTP transport."),
    ] = 8000,
) -> None:
    """Run the Moodle MCP server."""
    serve_mcp_server(http=http, host=host, port=port)


def serve_mcp_server(*, http: bool, host: str, port: int) -> None:
    """Run the shared FastMCP server with the selected transport."""
    mcp = create_server()
    if http:
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()
