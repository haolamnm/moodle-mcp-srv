"""CLI entry point for the Moodle MCP server."""

from __future__ import annotations

import argparse

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

    args = parser.parse_args()
    configure_logging()
    mcp = create_server()

    if args.http:
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
