"""Moodle API exceptions."""

from __future__ import annotations


class MoodleAPIError(Exception):
    """Raised when the Moodle API returns an error response."""

    def __init__(self, error_code: str, message: str, function: str) -> None:
        self.error_code = error_code
        self.message = message
        self.function = function
        super().__init__(f"Moodle API error [{error_code}] in {function}: {message}")
