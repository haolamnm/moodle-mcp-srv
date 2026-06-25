"""Moodle web service function names used by this server."""

from __future__ import annotations

from enum import StrEnum


class APIFunction(StrEnum):
    """Moodle web service function names used by this server."""

    # Core
    core_webservice_get_site_info = "core_webservice_get_site_info"
    core_enrol_get_users_courses = "core_enrol_get_users_courses"
    core_course_get_contents = "core_course_get_contents"
    core_calendar_get_calendar_upcoming_view = "core_calendar_get_calendar_upcoming_view"
    core_completion_get_activities_completion_status = (
        "core_completion_get_activities_completion_status"
    )
    core_completion_update_activity_completion_status_manually = (
        "core_completion_update_activity_completion_status_manually"
    )
    core_calendar_create_calendar_events = "core_calendar_create_calendar_events"
    core_files_get_files = "core_files_get_files"

    # Assignments
    mod_assign_get_assignments = "mod_assign_get_assignments"
    mod_assign_get_submission_status = "mod_assign_get_submission_status"
    mod_assign_save_submission = "mod_assign_save_submission"
    mod_assign_submit_for_grading = "mod_assign_submit_for_grading"

    # Grades
    gradereport_user_get_grade_items = "gradereport_user_get_grade_items"

    # Quiz
    mod_quiz_get_quizzes_by_courses = "mod_quiz_get_quizzes_by_courses"
    mod_quiz_get_user_attempts = "mod_quiz_get_user_attempts"
    mod_quiz_get_attempt_review = "mod_quiz_get_attempt_review"

    # Forum
    mod_forum_get_forums_by_courses = "mod_forum_get_forums_by_courses"
    mod_forum_get_forum_discussions = "mod_forum_get_forum_discussions"
    mod_forum_add_discussion_post = "mod_forum_add_discussion_post"
    mod_forum_add_discussion = "mod_forum_add_discussion"
