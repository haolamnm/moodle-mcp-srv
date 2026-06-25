"""Typed response model exports for Moodle MCP tools."""

from __future__ import annotations

from moodle_mcp.models.assignments import (
    Assignment,
    AssignmentFile,
    FeedbackGrade,
    SubmissionReceipt,
    SubmissionStatus,
)
from moodle_mcp.models.calendar import CalendarEvent, Deadline
from moodle_mcp.models.courses import Course, CourseSection, Module, SiteInfo
from moodle_mcp.models.dashboard import DashboardGrade, DashboardSummary, RecentActivity
from moodle_mcp.models.diagnostics import (
    DoctorCheck,
    DoctorReport,
    FeatureAvailability,
    ServerCapabilityReport,
    WriteReceipt,
)
from moodle_mcp.models.forums import AnnouncementPost, ForumDiscussion, ForumPost
from moodle_mcp.models.grades import CompletionActivity, GradeItem
from moodle_mcp.models.json import JsonArray, JsonObject, JsonValue, MoodleResponse
from moodle_mcp.models.quizzes import Quiz, QuizAttempt, QuizQuestionReview

__all__ = [
    "AnnouncementPost",
    "Assignment",
    "AssignmentFile",
    "CalendarEvent",
    "CompletionActivity",
    "Course",
    "CourseSection",
    "DashboardGrade",
    "DashboardSummary",
    "Deadline",
    "DoctorCheck",
    "DoctorReport",
    "FeatureAvailability",
    "FeedbackGrade",
    "ForumDiscussion",
    "ForumPost",
    "GradeItem",
    "JsonArray",
    "JsonObject",
    "JsonValue",
    "Module",
    "MoodleResponse",
    "Quiz",
    "QuizAttempt",
    "QuizQuestionReview",
    "RecentActivity",
    "ServerCapabilityReport",
    "SiteInfo",
    "SubmissionReceipt",
    "SubmissionStatus",
    "WriteReceipt",
]
