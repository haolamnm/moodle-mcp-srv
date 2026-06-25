"""Quiz MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

from moodle_mcp import api
from moodle_mcp.models import Quiz, QuizAttempt, QuizQuestionReview  # noqa: TC001

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register Quiz tools."""
    mcp.tool(get_quizzes)
    mcp.tool(get_quiz_attempts)
    mcp.tool(get_quiz_attempt_review)


async def get_quizzes(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[Quiz]:
    """Return quizzes across courses.

    Args:
        course_ids: Optional list of course IDs to filter by.
    Returns:
        Quizzes with name, open/close times, time limit, max grade.
    """
    return await api.get_quizzes(course_ids, limit)


async def get_quiz_attempts(quizid: int, limit: int = 20) -> list[QuizAttempt]:
    """Return all quiz attempts by the current user.

    Args:
        quizid: The quiz ID.
    Returns:
        Attempts with id, state, timestart, timefinish, grade.
    """
    return await api.get_quiz_attempts(quizid, limit)


async def get_quiz_attempt_review(
    attemptid: int,
    limit: int = 100,
) -> list[QuizQuestionReview]:
    """Return a detailed question-by-question review of a quiz attempt.

    Args:
        attemptid: The attempt ID (from get_quiz_attempts).
    Returns:
        Each question with number, text, your answer, correct answer, marks, feedback.
    """
    return await api.get_quiz_attempt_review(attemptid, limit)
