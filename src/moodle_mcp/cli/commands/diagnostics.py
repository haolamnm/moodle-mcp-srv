"""Diagnostic CLI commands."""

from __future__ import annotations

import asyncio
from typing import Annotated

import typer

from moodle_mcp import api


def doctor(
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Print a machine-readable DoctorReport."),
    ] = False,
    check_writes: Annotated[
        bool,
        typer.Option(
            "--check-writes",
            help="Include write Moodle Features in function availability checks.",
        ),
    ] = False,
) -> None:
    """Validate Moodle MCP configuration and Web Service setup."""
    report = asyncio.run(api.run_doctor(check_writes=check_writes))
    if json_output:
        typer.echo(report.model_dump_json())
    else:
        typer.echo(format_doctor_report(report))
    if not report.ok:
        raise typer.Exit(1)


def ping(
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Print Site Info as JSON."),
    ] = False,
) -> None:
    """Check that the configured Moodle token can read Site Info."""
    site_info = asyncio.run(api.get_site_info())
    if json_output:
        typer.echo(site_info.model_dump_json())
        return

    site_url = site_info.siteurl or "unknown URL"
    release = site_info.release or "unknown release"
    typer.echo(f"OK: {site_info.sitename} ({site_url}, {release})")


def format_doctor_report(report: api.DoctorReport) -> str:
    """Format a DoctorReport for terminal output."""
    lines = ["Moodle MCP Doctor"]
    if report.site_info is not None:
        site = report.site_info.siteurl or "unknown URL"
        release = report.site_info.release or "unknown release"
        lines.append(f"Site Info: {report.site_info.sitename} ({site}, {release})")

    for check in report.checks:
        label = check.status.upper()
        lines.append(f"{label}: {check.name} - {check.message}")
        if check.action is not None:
            lines.append(f"Action: {check.action}")

    if report.features is not None:
        missing = sorted(
            {
                function
                for feature in report.features.features
                for function in feature.missing_functions
            }
        )
        if missing:
            lines.append("Missing functions:")
            lines.extend(f"- {function}" for function in missing)
        if not report.check_writes:
            lines.append("Write checks: skipped (use --check-writes to include write functions).")

    return "\n".join(lines)
