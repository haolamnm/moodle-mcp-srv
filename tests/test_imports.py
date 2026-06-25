from __future__ import annotations

from moodle_mcp import api
from moodle_mcp.server import mcp


def test_api_package_reexports_tool_functions() -> None:
    tool_functions = [
        api.get_site_info,
        api.get_my_courses,
        api.get_course_content,
        api.get_calendar_events,
        api.dashboard_summary,
        api.get_assignments,
        api.get_assignment_details,
        api.get_assignment_files,
        api.submit_assignment,
        api.check_submission,
        api.get_feedback,
        api.get_grades,
        api.get_course_progress,
        api.get_upcoming_deadlines,
        api.get_quizzes,
        api.get_quiz_attempts,
        api.get_quiz_attempt_review,
        api.get_forum_discussions,
        api.post_forum_reply,
        api.create_forum_discussion,
        api.get_announcements,
    ]

    assert len(tool_functions) == 21


def test_server_exports_fastmcp_instance() -> None:
    assert mcp.name == "Moodle MCP"
