from __future__ import annotations

import pytest

from moodle_mcp import api
from moodle_mcp.tools.availability import raise_tool_error_for_moodle_failure


def test_missing_function_failure_yields_setup_message() -> None:
    exc = api.MoodleAPIError("invalidrecord", "no such record", "mod_assign_get_assignments")

    with pytest.raises(Exception, match="doctor") as exc_info:
        raise_tool_error_for_moodle_failure(exc, api.MoodleFeature.assignments)

    assert "Missing Moodle Web Service Function Name" in str(exc_info.value)


def test_access_denied_failure_yields_access_error_message() -> None:
    exc = api.MoodleAPIError("accessexception", "denied", "gradereport_user_get_grade_items")

    with pytest.raises(Exception, match="Moodle refused this request") as exc_info:
        raise_tool_error_for_moodle_failure(exc, api.MoodleFeature.grades)

    assert "accessexception" in str(exc_info.value)


def test_unknown_failure_falls_back_to_raw_error() -> None:
    exc = api.MoodleAPIError("invalidresponseexception", "weird", "mod_quiz_get_quizzes_by_courses")

    with pytest.raises(Exception, match="invalidresponseexception"):
        raise_tool_error_for_moodle_failure(exc, api.MoodleFeature.quizzes)
