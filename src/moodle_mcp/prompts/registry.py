"""FastMCP prompt registration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp.prompts import learning

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register reusable Moodle workflows."""
    learning.register(mcp)
