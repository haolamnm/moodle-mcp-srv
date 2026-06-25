"""Assignment response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Assignment(BaseModel):
    id: int
    cmid: int
    course: int
    name: str
    duedate: int | None
    cutoffdate: int | None
    allowsubmissionsfromdate: int | None
    grade: int | None
    timemodified: int | None
    intro: str | None
    introformat: int
    coursemodule: int | None


class AssignmentFile(BaseModel):
    filename: str
    filepath: str | None
    filesize: int
    mimetype: str | None
    fileurl: str | None
    timemodified: int | None


class SubmissionReceipt(BaseModel):
    status: str
    assignmentid: int
    dry_run: bool = False
    message: str | None = None
    data: str | None = None


class SubmissionStatus(BaseModel):
    status: str
    timemodified: int | None
    attemptnumber: int | None
    gradingstatus: str | None


class FeedbackGrade(BaseModel):
    grade: float | None
    maxgrade: float | None
    feedback_text: str | None = Field(
        default=None, description="Feedback text without Moodle internals."
    )
    timemodified: int | None
    grader: str | None
