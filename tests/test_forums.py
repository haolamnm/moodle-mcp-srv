from __future__ import annotations

import asyncio

import pytest

from moodle_mcp.api import forums
from moodle_mcp.moodle import APIFunction


def test_get_forum_discussions_uses_forum_discussions_function(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_function: APIFunction | None = None
    captured_params: dict[str, str] = {}

    async def fake_get_course_forums(courseid: int) -> list[dict[str, object]]:
        await asyncio.sleep(0)
        assert courseid == 10
        return [{"id": 5, "type": "general"}]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        nonlocal captured_function
        await asyncio.sleep(0)
        captured_function = function
        captured_params.update(params or {})
        return {
            "discussions": [
                {
                    "id": 7,
                    "name": "Welcome",
                    "userfullname": "Teacher",
                    "timemodified": 123,
                    "numreplies": 2,
                    "pinned": False,
                }
            ]
        }

    monkeypatch.setattr(forums, "_get_course_forums", fake_get_course_forums)
    monkeypatch.setattr(forums, "get_moodle_api_data", fake_get_moodle_api_data)

    discussions = asyncio.run(forums.get_forum_discussions(10))

    assert captured_function == APIFunction.mod_forum_get_forum_discussions
    assert captured_params == {"forumid": "5"}
    assert [discussion.name for discussion in discussions] == ["Welcome"]


def test_get_announcements_reads_news_forums(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [10]

    async def fake_get_course_forums(courseid: int) -> list[dict[str, object]]:
        await asyncio.sleep(0)
        assert courseid == 10
        return [
            {"id": 5, "type": "news", "name": "Announcements"},
            {"id": 6, "type": "general", "name": "General"},
        ]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_forum_get_forum_discussions
        assert params == {"forumid": "5"}
        return {
            "discussions": [
                {
                    "id": "7",
                    "name": "Exam notice",
                    "message": "<p>Read this</p>",
                    "userfullname": "Teacher",
                    "timemodified": "123",
                }
            ]
        }

    monkeypatch.setattr(forums, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(forums, "_get_course_forums", fake_get_course_forums)
    monkeypatch.setattr(forums, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(forums.get_announcements([10]))

    assert [announcement.model_dump() for announcement in result] == [
        {
            "id": 7,
            "subject": "Exam notice",
            "message": "<p>Read this</p>",
            "author": "Teacher",
            "timemodified": 123,
            "courseid": 10,
            "coursename": "Announcements",
        }
    ]


def test_forum_write_tools_default_to_dry_run() -> None:
    reply = asyncio.run(forums.post_forum_reply(1, "Message"))
    discussion = asyncio.run(forums.create_forum_discussion(2, "Subject", "Message"))

    assert reply.dry_run is True
    assert reply.action == "post_forum_reply"
    assert reply.target_id == 1
    assert discussion.dry_run is True
    assert discussion.action == "create_forum_discussion"
    assert discussion.target_id == 2


def test_forum_write_tools_require_reason_when_not_dry_run() -> None:
    with pytest.raises(ValueError, match="reason"):
        asyncio.run(forums.post_forum_reply(1, "Message", dry_run=False))

    with pytest.raises(ValueError, match="reason"):
        asyncio.run(forums.create_forum_discussion(2, "Subject", "Message", dry_run=False))


def test_forum_write_tools_call_moodle_when_confirmed(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[APIFunction, dict[str, str] | None]] = []

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        calls.append((function, params))
        if function == APIFunction.mod_forum_add_discussion_post:
            return {"postid": "11", "timemodified": "123"}
        return {"discussionid": "12", "timemodified": "456"}

    monkeypatch.setattr(forums, "get_moodle_api_data", fake_get_moodle_api_data)

    reply = asyncio.run(
        forums.post_forum_reply(1, "Message", "Subject", dry_run=False, reason="User confirmed")
    )
    discussion = asyncio.run(
        forums.create_forum_discussion(
            2, "Subject", "Message", dry_run=False, reason="User confirmed"
        )
    )

    assert calls == [
        (
            APIFunction.mod_forum_add_discussion_post,
            {
                "discussionid": "1",
                "postsubject": "Subject",
                "message": "Message",
                "messageformat": "1",
            },
        ),
        (
            APIFunction.mod_forum_add_discussion,
            {
                "forumid": "2",
                "subject": "Subject",
                "message": "Message",
                "messageformat": "1",
            },
        ),
    ]
    assert reply.changed == ["Created forum post 11."]
    assert discussion.changed == ["Created forum discussion 12."]
