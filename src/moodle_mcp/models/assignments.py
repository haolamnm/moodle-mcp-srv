"""Assignment response models."""

from __future__ import annotations

from pydantic import BaseModel, Field

from moodle_mcp.models.strings import (  # noqa: TC001
    MoodleFilePath,
    MoodleHtml,
    MoodleMimeType,
    MoodlePluginFileUrl,
    MoodleText,
)


class Assignment(BaseModel):
    id: int
    cmid: int
    course: int
    name: MoodleText
    duedate: int | None
    cutoffdate: int | None
    allowsubmissionsfromdate: int | None
    grade: int | None
    timemodified: int | None
    intro: MoodleHtml | None
    introformat: int
    coursemodule: int | None


class AssignmentFile(BaseModel):
    filename: MoodleText
    filepath: MoodleFilePath | None
    filesize: int
    mimetype: MoodleMimeType | None
    fileurl: MoodlePluginFileUrl | None
    timemodified: int | None


class SubmissionReceipt(BaseModel):
    status: str
    assignmentid: int
    dry_run: bool = False
    message: MoodleText | None = None
    data: MoodleText | None = None


class SubmissionStatus(BaseModel):
    status: MoodleText
    timemodified: int | None
    attemptnumber: int | None
    gradingstatus: str | None


class FeedbackGrade(BaseModel):
    grade: float | None
    maxgrade: float | None
    feedback_text: MoodleHtml | None = Field(
        default=None, description="Feedback text without Moodle internals."
    )
    timemodified: int | None
    grader: MoodleText | None
