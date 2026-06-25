"""Moodle request parameter helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def format_array_params(key: str, values: Sequence[int | str]) -> dict[str, str]:
    """Format a list as Moodle-style array parameters."""
    return {f"{key}[{i}]": str(v) for i, v in enumerate(values)}
