"""Configuration and logging exports."""

from __future__ import annotations

from moodle_mcp.config.logging import configure_logging
from moodle_mcp.config.settings import Settings, settings

__all__ = ["Settings", "configure_logging", "settings"]
