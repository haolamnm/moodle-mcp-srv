"""Public tool implementation API grouped by Moodle domain modules."""

from __future__ import annotations

from moodle_mcp.api.assignments import (
    check_submission,
    get_assignment_details,
    get_assignment_files,
    get_assignments,
    get_feedback,
    submit_assignment,
)
from moodle_mcp.api.calendar import get_calendar_events, get_upcoming_deadlines
from moodle_mcp.api.courses import get_course_content, get_my_courses, get_site_info
from moodle_mcp.api.dashboard import dashboard_summary
from moodle_mcp.api.forums import (
    create_forum_discussion,
    get_announcements,
    get_forum_discussions,
    post_forum_reply,
)
from moodle_mcp.api.grades import get_course_progress, get_grades
from moodle_mcp.api.quizzes import get_quiz_attempt_review, get_quiz_attempts, get_quizzes
from moodle_mcp.models import (
    AnnouncementPost,
    Assignment,
    AssignmentFile,
    CalendarEvent,
    CompletionActivity,
    Course,
    CourseSection,
    DashboardGrade,
    DashboardSummary,
    Deadline,
    FeedbackGrade,
    ForumDiscussion,
    ForumPost,
    GradeItem,
    Module,
    Quiz,
    QuizAttempt,
    QuizQuestionReview,
    RecentActivity,
    SiteInfo,
    SubmissionReceipt,
    SubmissionStatus,
)

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
    "FeedbackGrade",
    "ForumDiscussion",
    "ForumPost",
    "GradeItem",
    "Module",
    "Quiz",
    "QuizAttempt",
    "QuizQuestionReview",
    "RecentActivity",
    "SiteInfo",
    "SubmissionReceipt",
    "SubmissionStatus",
    "check_submission",
    "create_forum_discussion",
    "dashboard_summary",
    "get_announcements",
    "get_assignment_details",
    "get_assignment_files",
    "get_assignments",
    "get_calendar_events",
    "get_course_content",
    "get_course_progress",
    "get_feedback",
    "get_forum_discussions",
    "get_grades",
    "get_my_courses",
    "get_quiz_attempt_review",
    "get_quiz_attempts",
    "get_quizzes",
    "get_site_info",
    "get_upcoming_deadlines",
    "post_forum_reply",
    "submit_assignment",
]
