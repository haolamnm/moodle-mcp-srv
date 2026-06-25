from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, Any, Protocol, cast, runtime_checkable
from urllib.parse import parse_qsl

from dirty_equals import IsPartialDict
from fastmcp import Client
import httpx
import pytest

from moodle_mcp.api import reset_available_functions_cache
from moodle_mcp.moodle import client as moodle_client, reset_current_user_cache
from moodle_mcp.server import create_server

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock


MOODLE_URL = "https://moodle.test/webservice/rest/server.php"
MOODLE_TOKEN = "mock-token"


@runtime_checkable
class _TextResource(Protocol):
    text: str


def _form_data(request: httpx.Request) -> dict[str, str]:
    return dict(parse_qsl(request.content.decode()))


def _json_response(data: object) -> httpx.Response:
    return httpx.Response(200, json=data)


def _tool_payload(structured_content: object) -> object:
    if isinstance(structured_content, Mapping):
        content = cast("Mapping[str, object]", structured_content)
        if "result" in content:
            return content["result"]
        return content
    return structured_content


async def _call_ok(client: Client[Any], tool_name: str, arguments: dict[str, object]) -> object:
    result = await client.call_tool(tool_name, arguments)
    assert result.is_error is False, f"{tool_name} failed: {result.content}"
    return _tool_payload(result.structured_content)


def _first_id(items: object) -> int:
    assert isinstance(items, list)
    item = cast("list[object]", items)[0]
    assert isinstance(item, Mapping)
    item_map = cast("Mapping[str, object]", item)
    value = item_map["id"]
    assert isinstance(value, int)
    return value


def _resource_text(contents: object) -> str:
    assert isinstance(contents, list)
    item = cast("list[object]", contents)[0]
    assert isinstance(item, _TextResource)
    return item.text


def _install_mock_moodle(httpx_mock: HTTPXMock) -> list[dict[str, str]]:
    requests: list[dict[str, str]] = []

    def respond(request: httpx.Request) -> httpx.Response:
        form = _form_data(request)
        requests.append(form)
        assert form["wstoken"] == MOODLE_TOKEN
        assert form["moodlewsrestformat"] == "json"
        return _json_response(_response_for(form))

    httpx_mock.add_callback(respond, method="POST", url=MOODLE_URL, is_reusable=True)
    return requests


def _response_for(form: Mapping[str, str]) -> object:
    response_builder = _MOODLE_RESPONSES.get(form["wsfunction"])
    if response_builder is None:
        return {
            "exception": "moodle_exception",
            "errorcode": "mock_unhandled_function",
            "message": f"Unhandled mock wsfunction: {form['wsfunction']}",
        }
    return response_builder(form)


def _site_info_response(form: Mapping[str, str]) -> object:
    _ = form
    return {
        "sitename": "Mock Moodle",
        "siteurl": "https://moodle.test",
        "userid": 42,
        "username": "student",
        "firstname": "Ada",
        "lastname": "Lovelace",
        "fullname": "Ada Lovelace",
        "release": "5.0.1",
        "version": "2025041401",
        "functions": [{"name": name} for name in _MOODLE_FUNCTIONS],
    }


def _enrolled_courses_response(form: Mapping[str, str]) -> object:
    assert form["userid"] == "42"
    return [_course()]


def _course_content_response(form: Mapping[str, str]) -> object:
    assert form["courseid"] == "10"
    return [_course_section()]


def _calendar_response(form: Mapping[str, str]) -> object:
    _ = form
    return {"events": [_calendar_event(), _overdue_calendar_event()]}


def _assignments_response(form: Mapping[str, str]) -> object:
    assert form["courseids[0]"] == "10"
    return {"courses": [{**_course(), "assignments": [_assignment()]}]}


def _submission_status_response(form: Mapping[str, str]) -> object:
    assert form["assignid"] == "99"
    return _submission_status()


def _grades_response(form: Mapping[str, str]) -> object:
    assert form["courseid"] == "10"
    assert form["userid"] == "42"
    return {"gradeitems": [_grade_item()]}


def _completion_response(form: Mapping[str, str]) -> object:
    assert form["courseid"] == "10"
    assert form["userid"] == "42"
    return {"statuses": [_completion_status()]}


def _quizzes_response(form: Mapping[str, str]) -> object:
    assert form["courseids[0]"] == "10"
    return {"quizzes": [_quiz()]}


def _quiz_attempts_response(form: Mapping[str, str]) -> object:
    assert form["quizid"] == "55"
    assert form["userid"] == "42"
    return {"attempts": [_quiz_attempt()]}


def _quiz_review_response(form: Mapping[str, str]) -> object:
    assert form["attemptid"] == "66"
    return {"questions": [_quiz_question()]}


def _forums_response(form: Mapping[str, str]) -> object:
    assert form["courseids[0]"] == "10"
    return [_forum()]


def _forum_discussions_response(form: Mapping[str, str]) -> object:
    assert form["forumid"] == "77"
    return {"discussions": [_forum_discussion()]}


def _course() -> dict[str, object]:
    return {
        "id": 10,
        "fullname": "Algorithms",
        "shortname": "ALG",
        "category": 2,
        "summary": "Course summary",
        "startdate": 1_700_000_000,
        "enddate": 0,
        "progress": 50.0,
    }


def _course_section() -> dict[str, object]:
    return {
        "id": 20,
        "name": "Lecture",
        "summary": "",
        "modules": [
            {
                "id": 30,
                "name": "Homework 1",
                "modname": "assign",
                "url": "https://moodle.test/mod/assign/view.php?id=30",
                "description": "Read the prompt and submit your answer.",
            }
        ],
    }


def _calendar_event() -> dict[str, object]:
    return {
        "id": 80,
        "name": "Homework 1 due",
        "description": "Submit Homework 1.",
        "timestart": 1_782_921_600,
        "eventtype": "due",
        "course": {"id": 10, "fullname": "Algorithms"},
    }


def _overdue_calendar_event() -> dict[str, object]:
    return {
        "id": 81,
        "name": "Old event",
        "description": "",
        "timestart": 1,
        "eventtype": "due",
        "course": {"id": 10, "fullname": "Algorithms"},
    }


def _assignment() -> dict[str, object]:
    return {
        "id": 99,
        "cmid": 30,
        "course": 10,
        "name": "Homework 1",
        "duedate": 1_782_921_600,
        "cutoffdate": 1_782_921_600,
        "allowsubmissionsfromdate": 1_782_234_000,
        "grade": 10,
        "timemodified": 1_782_271_588,
        "intro": "<p>Read the prompt and submit your answer.</p>",
        "introformat": 1,
        "coursemodule": 30,
        "introfiles": [
            {
                "filename": "prompt.pdf",
                "filepath": "/",
                "filesize": 1234,
                "mimetype": "application/pdf",
                "fileurl": "https://moodle.test/pluginfile.php/1/prompt.pdf",
                "timemodified": 1_782_271_588,
            }
        ],
    }


def _submission_status() -> dict[str, object]:
    return {
        "lastattempt": {
            "submission": {
                "status": "submitted",
                "timemodified": 1_782_271_600,
                "attemptnumber": 0,
            }
        },
        "feedback": {
            "grade": {
                "grade": 8.5,
                "gradefordisplay": {"grade": 10},
                "timemodified": 1_782_271_700,
                "grader": {"fullname": "Teacher"},
            },
            "plugins": [{"editorfields": [{"text": "Good work."}]}],
        },
    }


def _grade_item() -> dict[str, object]:
    return {
        "id": 101,
        "itemname": "Homework 1",
        "graderaw": 8.5,
        "percentageformatted": "85.00 %",
        "lettergradeformatted": "B",
        "rangemin": 0,
        "rangemax": 10,
        "feedback": {"text": "Good work."},
    }


def _completion_status() -> dict[str, object]:
    return {
        "cmid": 30,
        "activityname": "Homework 1",
        "modname": "assign",
        "state": 1,
        "timecompleted": 1_782_271_700,
    }


def _quiz() -> dict[str, object]:
    return {
        "id": 55,
        "course": 10,
        "name": "Quiz 1",
        "timeopen": 1_782_234_000,
        "timeclose": 1_782_921_600,
        "timelimit": 1800,
        "grade": 10.0,
        "attempts": 2,
        "hasquestions": True,
    }


def _quiz_attempt() -> dict[str, object]:
    return {
        "id": 66,
        "state": "finished",
        "timestart": 1_782_271_000,
        "timefinish": 1_782_271_600,
        "sumgrades": 9.0,
        "grade": 9.0,
        "grademax": 10.0,
    }


def _quiz_question() -> dict[str, object]:
    return {
        "slot": 1,
        "html": {
            "questiontext": "What is 2 + 2?",
            "youranswer": "4",
            "correctanswer": "4",
            "feedback": "Correct.",
        },
        "marks": 1,
        "maxmark": 1,
    }


def _forum() -> dict[str, object]:
    return {"id": 77, "course": 10, "name": "Announcements", "type": "news"}


def _forum_discussion() -> dict[str, object]:
    return {
        "id": 88,
        "name": "Welcome",
        "message": "Welcome to class.",
        "userfullname": "Teacher",
        "timemodified": 1_782_271_800,
        "postcount": 1,
        "pinned": True,
    }


_MOODLE_RESPONSES: dict[str, Callable[[Mapping[str, str]], object]] = {
    "core_webservice_get_site_info": _site_info_response,
    "core_enrol_get_users_courses": _enrolled_courses_response,
    "core_course_get_contents": _course_content_response,
    "core_calendar_get_calendar_upcoming_view": _calendar_response,
    "mod_assign_get_assignments": _assignments_response,
    "mod_assign_get_submission_status": _submission_status_response,
    "gradereport_user_get_grade_items": _grades_response,
    "core_completion_get_activities_completion_status": _completion_response,
    "mod_quiz_get_quizzes_by_courses": _quizzes_response,
    "mod_quiz_get_user_attempts": _quiz_attempts_response,
    "mod_quiz_get_attempt_review": _quiz_review_response,
    "mod_forum_get_forums_by_courses": _forums_response,
    "mod_forum_get_forum_discussions": _forum_discussions_response,
}

_MOODLE_FUNCTIONS = sorted(
    {
        *_MOODLE_RESPONSES,
        "mod_assign_save_submission",
        "mod_forum_add_discussion_post",
        "mod_forum_add_discussion",
    }
)


@pytest.mark.asyncio
async def test_mcp_tools_and_resources_against_lightweight_mock_moodle(  # noqa: PLR0914, PLR0915
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests = _install_mock_moodle(httpx_mock)
    monkeypatch.setattr(moodle_client, "_get_config", lambda: (MOODLE_URL, MOODLE_TOKEN))
    reset_current_user_cache()
    reset_available_functions_cache()

    async with Client(create_server()) as client:
        site_info = await _call_ok(client, "get_site_info", {})
        assert site_info == IsPartialDict(sitename="Mock Moodle", userid=42, release="5.0.1")

        courses = await _call_ok(client, "get_my_courses", {})
        course_id = _first_id(courses)

        events = await _call_ok(client, "get_calendar_events", {"daysahead": 30, "limit": 20})
        assert events == [IsPartialDict(id=80, name="Homework 1 due")]

        deadlines = await _call_ok(
            client,
            "get_upcoming_deadlines",
            {"daysahead": 30, "limit": 20},
        )
        assert deadlines == [
            IsPartialDict(type="assignment", id=99, name="Homework 1", course="Algorithms"),
            IsPartialDict(type="quiz", id=55, name="Quiz 1", course="Algorithms"),
        ]

        assignments = await _call_ok(
            client,
            "get_assignments",
            {"course_ids": [course_id], "limit": 20},
        )
        assignment_id = _first_id(assignments)

        await _call_ok(client, "get_assignment_details", {"assignmentid": assignment_id})
        files = await _call_ok(client, "get_assignment_files", {"assignmentid": assignment_id})
        assert files == [IsPartialDict(filename="prompt.pdf")]
        await _call_ok(client, "check_submission", {"assignmentid": assignment_id})
        await _call_ok(client, "get_feedback", {"assignmentid": assignment_id})
        await _call_ok(
            client,
            "submit_assignment",
            {"assignmentid": assignment_id, "text": "Dry run only."},
        )

        await _call_ok(client, "dashboard_summary", {})
        await _call_ok(client, "get_course_content", {"courseid": course_id})
        await _call_ok(client, "get_grades", {"course_ids": [course_id], "limit": 20})
        await _call_ok(client, "get_course_progress", {"courseid": course_id, "limit": 20})
        await _call_ok(client, "get_announcements", {"course_ids": [course_id], "limit": 20})
        await _call_ok(client, "get_forum_discussions", {"courseid": course_id, "limit": 20})

        quizzes = await _call_ok(client, "get_quizzes", {"course_ids": [course_id], "limit": 20})
        quiz_id = _first_id(quizzes)
        attempts = await _call_ok(client, "get_quiz_attempts", {"quizid": quiz_id, "limit": 20})
        attempt_id = _first_id(attempts)
        await _call_ok(client, "get_quiz_attempt_review", {"attemptid": attempt_id, "limit": 20})

        await _call_ok(
            client,
            "post_forum_reply",
            {"discussionid": 88, "message": "Dry run only."},
        )
        await _call_ok(
            client,
            "create_forum_discussion",
            {"forumid": 77, "subject": "Dry run", "message": "Dry run only."},
        )

        course_resource = await client.read_resource(f"moodle://courses/{course_id}/content")
        course_overview_resource = await client.read_resource(
            f"moodle://courses/{course_id}/overview"
        )
        course_assignments_resource = await client.read_resource(
            f"moodle://courses/{course_id}/assignments"
        )
        grade_schema_resource = await client.read_resource(f"moodle://grades/{course_id}/schema")
        assignment_resource = await client.read_resource(
            f"moodle://assignments/{assignment_id}/brief"
        )
        site_profile_resource = await client.read_resource("moodle://site/profile")
        site_features_resource = await client.read_resource("moodle://site/features")

    assert _resource_text(course_resource).startswith("[")
    assert _resource_text(course_overview_resource).startswith("{")
    assert _resource_text(course_assignments_resource).startswith("[")
    assert _resource_text(grade_schema_resource).startswith("[")
    assert _resource_text(assignment_resource).startswith("{")
    assert _resource_text(site_profile_resource).startswith("{")
    assert _resource_text(site_features_resource).startswith("{")
    assert {request["wsfunction"] for request in requests} >= {
        "core_webservice_get_site_info",
        "core_enrol_get_users_courses",
        "core_course_get_contents",
        "mod_assign_get_assignments",
        "mod_assign_get_submission_status",
        "mod_forum_get_forum_discussions",
    }
    assert any(request.get("assignid") == "99" for request in requests)
    assert not any(request.get("assignmentid") == "99" for request in requests)
