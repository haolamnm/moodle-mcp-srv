"""Quiz tool implementations."""

from __future__ import annotations

from moodle_mcp.api._helpers import get_course_ids, limit_items
from moodle_mcp.api.coercion import (
    as_bool,
    as_int,
    as_object,
    as_optional_float,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import JsonObject, Quiz, QuizAttempt, QuizQuestionReview
from moodle_mcp.moodle import (
    APIFunction,
    format_array_params,
    get_moodle_api_data,
    resolve_current_user_id,
)


async def get_quizzes(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[Quiz]:
    """Return quizzes across courses."""
    cids = await get_course_ids(course_ids)
    if not cids:
        return []

    data = await get_moodle_api_data(
        APIFunction.mod_quiz_get_quizzes_by_courses,
        format_array_params("courseids", cids),
    )
    if not isinstance(data, dict):
        return []

    quizzes: list[Quiz] = []
    for quiz in object_list(data.get("quizzes")):
        quizzes.append(
            Quiz(
                id=as_int(quiz.get("id")),
                course=as_int(quiz.get("course")),
                name=as_str(quiz.get("name")),
                timeopen=as_optional_int(quiz.get("timeopen")),
                timeclose=as_optional_int(quiz.get("timeclose")),
                timelimit=as_optional_int(quiz.get("timelimit")),
                maxgrade=as_optional_float(quiz.get("grade")),
                attemptsallowed=as_optional_int(quiz.get("attempts")),
                hasquestions=as_bool(quiz.get("hasquestions")),
            )
        )
    return limit_items(quizzes, limit)


async def get_quiz_attempts(quizid: int, limit: int = 20) -> list[QuizAttempt]:
    """Return all attempts for a quiz by the current user."""
    userid = await resolve_current_user_id()
    data = await get_moodle_api_data(
        APIFunction.mod_quiz_get_user_attempts,
        {"quizid": str(quizid), "userid": str(userid)},
    )
    if not isinstance(data, dict):
        return []

    attempts: list[QuizAttempt] = []
    for attempt in object_list(data.get("attempts")):
        maxgrade = as_optional_float(attempt.get("grademax"))
        if maxgrade is None:
            maxgrade = as_optional_float(attempt.get("maxgrade"))

        attempts.append(
            QuizAttempt(
                id=as_int(attempt.get("id")),
                state=as_str(attempt.get("state")),
                timestart=as_optional_int(attempt.get("timestart")),
                timefinish=as_optional_int(attempt.get("timefinish")),
                sumgrades=as_optional_float(attempt.get("sumgrades")),
                grade=as_optional_float(attempt.get("grade")),
                maxgrade=maxgrade,
            )
        )
    return limit_items(attempts, limit)


async def get_quiz_attempt_review(
    attemptid: int,
    limit: int = 100,
) -> list[QuizQuestionReview]:
    """Return a detailed review of all questions in a quiz attempt."""
    data = await get_moodle_api_data(
        APIFunction.mod_quiz_get_attempt_review,
        {"attemptid": str(attemptid)},
    )
    if not isinstance(data, dict):
        return []

    questions: list[QuizQuestionReview] = []
    for question in object_list(data.get("questions")):
        html = as_object(question.get("html"))
        questions.append(
            QuizQuestionReview(
                number=as_int(question.get("slot")),
                questiontext=as_str(html.get("questiontext")),
                youranswer=_extract_answer(question, "youranswer"),
                correctanswer=_extract_answer(question, "correctanswer"),
                marks=as_optional_float(question.get("marks")),
                maxmarks=as_optional_float(question.get("maxmark")),
                feedback=as_optional_str(html.get("feedback")),
            )
        )
    return limit_items(questions, limit)


def _extract_answer(question: JsonObject, key: str) -> str:
    """Extract answer text from a question's html dict or plain text."""
    html = as_object(question.get("html"))
    if key in html:
        return as_str(html.get(key))
    return as_str(question.get(key))
