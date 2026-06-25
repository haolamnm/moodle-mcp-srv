from __future__ import annotations

from collections.abc import Mapping, Sequence
import os
from typing import Any, cast

from fastmcp import Client
import pytest

from moodle_mcp.server import create_server

pytestmark = pytest.mark.live_moodle


async def _call_ok(client: Client[Any], tool_name: str, arguments: dict[str, object]) -> object:
    result = await client.call_tool(tool_name, arguments)
    assert result.is_error is False, f"{tool_name} failed: {result.content}"
    return _tool_payload(result.structured_content)


def _tool_payload(structured_content: object) -> object:
    if isinstance(structured_content, Mapping):
        content = cast("Mapping[str, object]", structured_content)
        if "result" in content:
            return content["result"]
        return content
    return structured_content


def _first_int_field(items: object, field: str) -> int | None:
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        return None

    typed_items = cast("Sequence[object]", items)
    for item in typed_items:
        if isinstance(item, Mapping):
            item_map = cast("Mapping[str, object]", item)
            value = item_map.get(field)
            if isinstance(value, int):
                return value
    return None


@pytest.mark.asyncio
async def test_live_moodle_read_tools_and_dry_run_write_tools() -> None:
    if os.environ.get("MOODLE_MCP_RUN_LIVE_TESTS") != "1":
        pytest.skip("set MOODLE_MCP_RUN_LIVE_TESTS=1 to call the configured Moodle site")

    async with Client(create_server()) as client:
        await _call_ok(client, "get_site_info", {})
        courses = await _call_ok(client, "get_my_courses", {})
        course_id = _first_int_field(courses, "id")
        assert course_id is not None

        await _call_ok(client, "get_calendar_events", {"daysahead": 30, "limit": 20})
        await _call_ok(client, "get_upcoming_deadlines", {"daysahead": 30, "limit": 20})
        await _call_ok(client, "dashboard_summary", {})
        await _call_ok(client, "get_course_content", {"courseid": course_id})
        await _call_ok(client, "get_grades", {"course_ids": [course_id], "limit": 20})
        await _call_ok(client, "get_course_progress", {"courseid": course_id, "limit": 20})
        await _call_ok(client, "get_announcements", {"course_ids": [course_id], "limit": 20})
        await _call_ok(client, "get_forum_discussions", {"courseid": course_id, "limit": 20})

        assignments = await _call_ok(
            client,
            "get_assignments",
            {"course_ids": [course_id], "limit": 20},
        )
        assignment_id = _first_int_field(assignments, "id")
        if assignment_id is not None:
            await _call_ok(client, "get_assignment_details", {"assignmentid": assignment_id})
            await _call_ok(client, "get_assignment_files", {"assignmentid": assignment_id})
            await _call_ok(client, "check_submission", {"assignmentid": assignment_id})
            await _call_ok(client, "get_feedback", {"assignmentid": assignment_id})
            await _call_ok(
                client,
                "submit_assignment",
                {"assignmentid": assignment_id, "text": "Live smoke dry run only."},
            )

        quizzes = await _call_ok(client, "get_quizzes", {"course_ids": [course_id], "limit": 20})
        quiz_id = _first_int_field(quizzes, "id")
        if quiz_id is not None:
            attempts = await _call_ok(client, "get_quiz_attempts", {"quizid": quiz_id, "limit": 20})
            attempt_id = _first_int_field(attempts, "id")
            if attempt_id is not None:
                await _call_ok(
                    client,
                    "get_quiz_attempt_review",
                    {"attemptid": attempt_id, "limit": 20},
                )

        await _call_ok(
            client,
            "post_forum_reply",
            {"discussionid": 1, "message": "Live smoke dry run only."},
        )
        await _call_ok(
            client,
            "create_forum_discussion",
            {"forumid": 1, "subject": "Live smoke dry run", "message": "Dry run only."},
        )
