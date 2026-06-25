"""CLI entry point for the Moodle MCP server."""

from __future__ import annotations

import argparse
import asyncio

from moodle_mcp import api
from moodle_mcp.config import configure_logging
from moodle_mcp.server import create_server


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="moodle-mcp",
        description="Your Moodle dashboard, available to AI.",
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Run over HTTP transport (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host for HTTP transport (default: 127.0.0.1)",
    )
    subparsers = parser.add_subparsers(dest="command")
    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Validate Moodle MCP configuration and Web Service setup.",
    )
    doctor_parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Print a machine-readable DoctorReport.",
    )
    doctor_parser.add_argument(
        "--check-writes",
        action="store_true",
        help="Include write Moodle Features in function availability checks.",
    )

    args = parser.parse_args()
    configure_logging()

    if args.command == "doctor":
        report = asyncio.run(api.run_doctor(check_writes=args.check_writes))
        if args.json_output:
            print(report.model_dump_json())
        else:
            print(_format_doctor_report(report))
        if not report.ok:
            raise SystemExit(1)
        return

    mcp = create_server()

    if args.http:
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()


def _format_doctor_report(report: api.DoctorReport) -> str:
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


if __name__ == "__main__":
    main()
