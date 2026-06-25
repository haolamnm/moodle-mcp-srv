from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import quizzes
from moodle_mcp.moodle import APIFunction

if TYPE_CHECKING:
    import pytest


def test_get_quizzes_formats_quizzes(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, str] = {}

    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [10]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_quiz_get_quizzes_by_courses
        captured_params.update(params or {})
        return {
            "quizzes": [
                {
                    "id": "1",
                    "course": "10",
                    "name": "Quiz 1",
                    "timeopen": "100",
                    "timeclose": "200",
                    "timelimit": "60",
                    "grade": "10",
                    "attempts": "2",
                    "hasquestions": "1",
                }
            ]
        }

    monkeypatch.setattr(quizzes, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(quizzes, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(quizzes.get_quizzes([10]))

    assert captured_params == {"courseids[0]": "10"}
    assert [quiz.model_dump() for quiz in result] == [
        {
            "id": 1,
            "course": 10,
            "name": "Quiz 1",
            "timeopen": 100,
            "timeclose": 200,
            "timelimit": 60,
            "maxgrade": 10.0,
            "attemptsallowed": 2,
            "hasquestions": True,
        }
    ]


def test_get_quizzes_returns_empty_for_no_courses(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        _ = course_ids
        return []

    monkeypatch.setattr(quizzes, "get_course_ids", fake_get_course_ids)

    assert asyncio.run(quizzes.get_quizzes()) == []


def test_get_quiz_attempts_formats_attempts(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_quiz_get_user_attempts
        assert params == {"quizid": "5", "userid": "42"}
        return {
            "attempts": [
                {
                    "id": "9",
                    "state": "finished",
                    "timestart": "100",
                    "timefinish": "200",
                    "sumgrades": "7.5",
                    "grade": "8",
                    "maxgrade": "10",
                }
            ]
        }

    monkeypatch.setattr(quizzes, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(quizzes, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(quizzes.get_quiz_attempts(5))

    assert [attempt.model_dump() for attempt in result] == [
        {
            "id": 9,
            "state": "finished",
            "timestart": 100,
            "timefinish": 200,
            "sumgrades": 7.5,
            "grade": 8.0,
            "maxgrade": 10.0,
        }
    ]


def test_get_quiz_attempt_review_formats_questions(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_quiz_get_attempt_review
        assert params == {"attemptid": "9"}
        return {
            "questions": [
                {
                    "slot": "1",
                    "html": {
                        "questiontext": "<p>2 + 2?</p>",
                        "youranswer": "4",
                        "feedback": "Correct",
                    },
                    "correctanswer": "4",
                    "marks": "1",
                    "maxmark": "1",
                }
            ]
        }

    monkeypatch.setattr(quizzes, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(quizzes.get_quiz_attempt_review(9))

    assert [question.model_dump() for question in result] == [
        {
            "number": 1,
            "questiontext": "<p>2 + 2?</p>",
            "youranswer": "4",
            "correctanswer": "4",
            "marks": 1.0,
            "maxmarks": 1.0,
            "feedback": "Correct",
        }
    ]


def test_quiz_readers_return_empty_for_unexpected_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        _ = course_ids
        return [10]

    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        _ = function, params
        return []

    monkeypatch.setattr(quizzes, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(quizzes, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(quizzes, "get_moodle_api_data", fake_get_moodle_api_data)

    assert asyncio.run(quizzes.get_quizzes()) == []
    assert asyncio.run(quizzes.get_quiz_attempts(5)) == []
    assert asyncio.run(quizzes.get_quiz_attempt_review(9)) == []
