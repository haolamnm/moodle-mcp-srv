from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING

from moodle_mcp import api
from moodle_mcp.models import Deadline, ForumDiscussion, Quiz
from moodle_mcp.resources import courses, forums, quizzes

if TYPE_CHECKING:
    import pytest


def test_quiz_brief_resource_serializes_course_quizzes(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_quizzes(course_ids: list[int]) -> list[Quiz]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [
            Quiz(
                id=1,
                course=10,
                name="Quiz 1",
                timeopen=None,
                timeclose=None,
                timelimit=None,
                maxgrade=None,
                attemptsallowed=None,
                hasquestions=True,
            )
        ]

    monkeypatch.setattr(api, "get_quizzes", fake_get_quizzes)

    payload = json.loads(asyncio.run(quizzes.quiz_brief_resource(10)))

    assert [quiz["name"] for quiz in payload] == ["Quiz 1"]


def test_forum_digest_resource_serializes_discussions(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_forum_discussions(courseid: int) -> list[ForumDiscussion]:
        await asyncio.sleep(0)
        assert courseid == 10
        return [
            ForumDiscussion(
                id=7,
                name="Welcome",
                author="Teacher",
                timemodified=123,
                postcount=2,
                pinned=False,
            )
        ]

    monkeypatch.setattr(api, "get_forum_discussions", fake_get_forum_discussions)

    payload = json.loads(asyncio.run(forums.forum_digest_resource(10)))

    assert [discussion["name"] for discussion in payload] == ["Welcome"]


def test_upcoming_deadlines_resource_serializes_deadlines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_upcoming_deadlines() -> list[Deadline]:
        await asyncio.sleep(0)
        return [
            Deadline(
                type="assignment",
                id=99,
                name="Essay",
                course="Course",
                duedate=1_000_000,
                daysremaining=2,
            )
        ]

    monkeypatch.setattr(api, "get_upcoming_deadlines", fake_get_upcoming_deadlines)

    payload = json.loads(asyncio.run(courses.upcoming_deadlines_resource()))

    assert [deadline["name"] for deadline in payload] == ["Essay"]
