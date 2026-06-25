from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from dirty_equals import IsPartialDict, IsStr
from fastmcp import Client
from inline_snapshot import snapshot
import pytest

from moodle_mcp.server import create_server, mcp
from moodle_mcp.tools import assignments, courses, forums, grades, quizzes

if TYPE_CHECKING:
    from types import ModuleType

EXPECTED_TOOL_NAMES = {
    "check_submission",
    "create_calendar_event",
    "create_forum_discussion",
    "dashboard_summary",
    "get_announcements",
    "get_assignment_details",
    "get_assignment_files",
    "get_assignments",
    "get_calendar_events",
    "get_course_content",
    "get_course_progress",
    "get_feedback",
    "get_forum_discussions",
    "get_grades",
    "get_my_courses",
    "get_quiz_attempt_review",
    "get_quiz_attempts",
    "get_quizzes",
    "get_site_info",
    "get_upcoming_deadlines",
    "mark_activity_complete",
    "post_forum_reply",
    "submit_assignment",
}


def test_server_registers_expected_tools() -> None:
    tools = asyncio.run(mcp.list_tools())

    assert {tool.name for tool in tools} == EXPECTED_TOOL_NAMES


@pytest.mark.asyncio
async def test_mcp_contracts_are_stable() -> None:
    async with Client(create_server()) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
        prompts = await client.list_prompts()

    assert sorted(tool.name for tool in tools) == snapshot(sorted(EXPECTED_TOOL_NAMES))
    assert sorted(str(resource.uri) for resource in resources) == snapshot(
        [
            "moodle://dashboard/summary",
            "moodle://deadlines/upcoming",
            "moodle://site/features",
            "moodle://site/profile",
        ]
    )
    assert sorted(template.uriTemplate for template in resource_templates) == snapshot(
        [
            "moodle://assignments/{assignmentid}/brief",
            "moodle://courses/{courseid}/assignments",
            "moodle://courses/{courseid}/content",
            "moodle://courses/{courseid}/overview",
            "moodle://forums/{courseid}/digest",
            "moodle://grades/{courseid}/schema",
            "moodle://quizzes/{courseid}/brief",
        ]
    )
    assert sorted(prompt.name for prompt in prompts) == snapshot(
        [
            "investigate_missing_submission",
            "plan_assignment_work",
            "prepare_weekly_brief",
        ]
    )


@pytest.mark.asyncio
async def test_submit_assignment_defaults_to_dry_run() -> None:
    async with Client(create_server()) as client:
        result = await client.call_tool(
            "submit_assignment",
            {"assignmentid": 99, "text": "Final answer"},
        )

    assert result.is_error is False
    assert result.structured_content == IsPartialDict(
        dry_run=True,
        action="submit_assignment",
        target_id=99,
        warnings=[IsStr()],
    )


@pytest.mark.parametrize(
    ("module", "name", "args", "kwargs"),
    [
        (courses, "get_my_courses", (), {}),
        (courses, "get_site_info", (), {}),
        (courses, "get_course_content", (10,), {}),
        (courses, "get_calendar_events", (3, 50), {}),
        (courses, "create_calendar_event", ("Study", 1_000_000, None, True, None), {}),
        (courses, "dashboard_summary", (), {}),
        (assignments, "get_assignments", ([10], 50), {}),
        (assignments, "get_assignment_details", (99,), {}),
        (assignments, "get_assignment_files", (99,), {}),
        (assignments, "submit_assignment", (99, "Done", True, True, None), {}),
        (assignments, "check_submission", (99,), {}),
        (assignments, "get_feedback", (99,), {}),
        (grades, "get_grades", ([10], 100), {}),
        (grades, "get_course_progress", (10, 100), {}),
        (grades, "mark_activity_complete", (5, True, True, None), {}),
        (grades, "get_upcoming_deadlines", (7, 50), {}),
        (quizzes, "get_quizzes", ([10], 50), {}),
        (quizzes, "get_quiz_attempts", (55, 20), {}),
        (quizzes, "get_quiz_attempt_review", (66, 100), {}),
        (forums, "get_forum_discussions", (10, 20, 50), {}),
        (forums, "post_forum_reply", (30, "Message", "Subject", True, None), {}),
        (forums, "create_forum_discussion", (40, "Subject", "Message", True, None), {}),
        (forums, "get_announcements", ([10], 50), {}),
    ],
)
def test_tool_wrappers_delegate_to_api(
    module: ModuleType,
    name: str,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    async def fake_api_call(*call_args: Any, **call_kwargs: Any) -> str:
        await asyncio.sleep(0)
        calls.append((call_args, call_kwargs))
        return "sentinel"

    monkeypatch.setattr(module.api, name, fake_api_call)
    if hasattr(module, "require_feature"):

        async def fake_require_feature(feature: object) -> None:
            await asyncio.sleep(0)
            _ = feature

        monkeypatch.setattr(module, "require_feature", fake_require_feature)

    result = asyncio.run(getattr(module, name)(*args, **kwargs))

    assert result == "sentinel"
    assert calls == [(args, kwargs)]
