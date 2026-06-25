"""Typer application composition."""

from __future__ import annotations

from typing import Annotated

import typer

from moodle_mcp.cli.commands.serve import serve_mcp_server
from moodle_mcp.cli.registry import register_commands
from moodle_mcp.config import configure_logging

app = typer.Typer(
    help="Your Moodle dashboard, available to AI.",
    invoke_without_command=True,
    no_args_is_help=False,
    pretty_exceptions_show_locals=False,
)


@app.callback()
def root(
    ctx: typer.Context,
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
    """Run the MCP server when no subcommand is provided."""
    configure_logging()
    if ctx.invoked_subcommand is None:
        serve_mcp_server(http=http, host=host, port=port)


register_commands(app)


def main() -> None:
    """Run the Moodle MCP CLI."""
    app()


if __name__ == "__main__":
    main()
