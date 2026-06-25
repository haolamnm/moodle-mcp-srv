from __future__ import annotations

import asyncio

import pytest

from moodle_mcp.api import features
from moodle_mcp.moodle import APIFunction


def test_build_capability_report_marks_missing_functions() -> None:
    report = features.build_capability_report(
        {
            APIFunction.core_webservice_get_site_info.value,
            APIFunction.core_enrol_get_users_courses.value,
        },
        include_writes=False,
    )

    assignments = next(
        item for item in report.features if item.feature == features.MoodleFeature.assignments
    )

    assert report.available_functions_known is True
    assert assignments.status == "missing_function"
    assert assignments.missing_functions == [APIFunction.mod_assign_get_assignments.value]


def test_build_capability_report_marks_unknown_without_function_metadata() -> None:
    report = features.build_capability_report(None)

    assert report.available_functions_known is False
    assert {item.status for item in report.features} == {"unknown"}


def test_required_function_names_uses_exact_moodle_names() -> None:
    assert features.required_function_names(features.MoodleFeature.write_forum) == [
        "mod_forum_add_discussion_post",
        "mod_forum_add_discussion",
    ]


def test_feature_unavailable_error_message_is_actionable() -> None:
    message = features.feature_unavailable_message(
        features.MoodleFeature.forums,
        ["mod_forum_get_forums_by_courses"],
    )

    assert "mod_forum_get_forums_by_courses" in message
    assert "moodle-mcp doctor" in message


def test_classify_failure_separates_setup_from_access() -> None:
    assert features.classify_failure("invalidrecord") is features.FailureKind.missing_function
    assert features.classify_failure("accessexception") is features.FailureKind.access_denied
    assert features.classify_failure("nopermissions") is features.FailureKind.access_denied
    assert features.classify_failure("invalidresponseexception") is features.FailureKind.unknown


def test_access_error_message_avoids_authorization_claims() -> None:
    message = features.access_error_message(features.MoodleFeature.grades, "accessexception")

    assert "accessexception" in message
    assert "moodle-mcp doctor" in message
    assert "Moodle enforces this" in message


def test_ensure_feature_available_raises_for_known_missing_function(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_available_functions() -> frozenset[str]:
        await asyncio.sleep(0)
        return frozenset({APIFunction.core_webservice_get_site_info.value})

    monkeypatch.setattr(features, "get_available_functions", fake_get_available_functions)

    with pytest.raises(features.UnavailableFeatureError) as exc_info:
        asyncio.run(features.ensure_feature_available(features.MoodleFeature.assignments))

    assert exc_info.value.missing_functions == [APIFunction.mod_assign_get_assignments.value]
