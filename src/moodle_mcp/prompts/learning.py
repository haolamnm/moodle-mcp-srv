"""Student-facing Moodle workflow prompts."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP


def register(mcp: FastMCP) -> None:
    """Register student-facing workflow prompts."""
    mcp.prompt(prepare_weekly_brief)
    mcp.prompt(investigate_missing_submission)
    mcp.prompt(plan_assignment_work)


def prepare_weekly_brief() -> str:
    """Guide an agent through a read-only weekly Moodle briefing."""
    return "Prepare a read-only weekly Moodle brief. Start with dashboard_summary, then inspect upcoming deadlines and calendar events. Do not submit assignments or post forum content."


def investigate_missing_submission(course_name: str, assignment_name: str) -> str:
    """Guide an agent through a read-only missing-submission investigation."""
    return f"Investigate a possible missing submission for {assignment_name} in {course_name}. Find the course, inspect the assignment, check submission status, and summarize next steps. Do not submit work or modify Moodle."


def plan_assignment_work(course_name: str, assignment_name: str) -> str:
    """Guide an agent through assignment planning without writes."""
    return f"Help plan work for {assignment_name} in {course_name}. Read the assignment brief, files, due dates, and calendar context. Produce a short action plan. Do not submit the assignment."
