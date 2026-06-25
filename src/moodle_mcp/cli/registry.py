"""CLI command registration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp.cli.commands import doctor, inspect_server, ping, serve

if TYPE_CHECKING:
    import typer


def register_commands(app: typer.Typer) -> None:
    """Register all CLI subcommands."""
    app.command("serve")(serve)
    app.command("doctor")(doctor)
    app.command("ping")(ping)
    app.command("inspect")(inspect_server)
