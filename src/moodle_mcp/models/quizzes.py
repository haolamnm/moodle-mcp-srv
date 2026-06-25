"""Quiz response models."""

from __future__ import annotations

from pydantic import BaseModel


class Quiz(BaseModel):
    id: int
    course: int
    name: str
    timeopen: int | None
    timeclose: int | None
    timelimit: int | None
    maxgrade: float | None
    attemptsallowed: int | None
    hasquestions: bool


class QuizAttempt(BaseModel):
    id: int
    state: str
    timestart: int | None
    timefinish: int | None
    sumgrades: float | None
    grade: float | None
    maxgrade: float | None


class QuizQuestionReview(BaseModel):
    number: int
    questiontext: str
    youranswer: str
    correctanswer: str
    marks: float | None
    maxmarks: float | None
    feedback: str | None
