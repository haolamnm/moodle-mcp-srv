"""Dashboard Summary tool implementation."""

from __future__ import annotations

from moodle_mcp.api._helpers import DAYS_SECONDS, days_remaining, now_ts
from moodle_mcp.api.assignments import get_assignments
from moodle_mcp.api.courses import get_my_courses
from moodle_mcp.api.grades import get_grades
from moodle_mcp.models import Assignment, DashboardGrade, DashboardSummary, Deadline
from moodle_mcp.moodle import MoodleAPIError


async def dashboard_summary() -> DashboardSummary:
    """Aggregate overdue assignments, upcoming assignments, and new grades.

    Each section degrades independently: if a Moodle Web Service Function Name is
    unavailable or refused, that section is skipped and a warning is recorded
    instead of failing the whole summary.
    """
    current = now_ts()
    warnings: list[str] = []

    try:
        courses = await get_my_courses()
    except MoodleAPIError as exc:
        return DashboardSummary(
            overdue=[],
            due_today=[],
            due_this_week=[],
            new_grades=[],
            recent_activity=[],
            total_pending=0,
            warnings=[_section_warning("courses", exc)],
        )

    course_ids = [course.id for course in courses]
    course_map = {course.id: course.fullname for course in courses}

    overdue: list[Deadline] = []
    due_today: list[Deadline] = []
    due_this_week: list[Deadline] = []
    try:
        overdue, due_today, due_this_week = _assignment_windows(
            assignments=await get_assignments(course_ids),
            course_map=course_map,
            current=current,
        )
    except MoodleAPIError as exc:
        warnings.append(_section_warning("assignments", exc))

    new_grades, grade_warning = await _new_grades(course_ids)
    if grade_warning is not None:
        warnings.append(grade_warning)

    return DashboardSummary(
        overdue=overdue,
        due_today=due_today,
        due_this_week=due_this_week,
        new_grades=new_grades,
        recent_activity=[],
        total_pending=len(overdue) + len(due_today) + len(due_this_week),
        warnings=warnings,
    )


def _section_warning(section: str, exc: MoodleAPIError) -> str:
    """Build a privacy-safe warning that names the skipped section and error code."""
    return f"Skipped {section}: Moodle returned [{exc.error_code}]."


def _assignment_windows(
    assignments: list[Assignment],
    course_map: dict[int, str],
    current: int,
) -> tuple[list[Deadline], list[Deadline], list[Deadline]]:
    overdue: list[Deadline] = []
    due_today: list[Deadline] = []
    due_this_week: list[Deadline] = []

    day_start = current - (current % DAYS_SECONDS)
    tomorrow_start = day_start + DAYS_SECONDS
    week_end = day_start + 7 * DAYS_SECONDS

    for assignment in assignments:
        due = assignment.duedate
        if due is None or due <= 0:
            continue

        item = _assignment_deadline(assignment, course_map, due, current)
        if due < current:
            overdue.append(item)
        elif day_start <= due < tomorrow_start:
            due_today.append(item)
        elif due < week_end:
            due_this_week.append(item)

    return overdue, due_today, due_this_week


def _assignment_deadline(
    assignment: Assignment,
    course_map: dict[int, str],
    due: int,
    current: int,
) -> Deadline:
    return Deadline(
        type="assignment",
        id=assignment.id,
        name=assignment.name,
        course=course_map.get(assignment.course, ""),
        duedate=due,
        daysremaining=days_remaining(due, current),
    )


async def _new_grades(course_ids: list[int]) -> tuple[list[DashboardGrade], str | None]:
    new_grades: list[DashboardGrade] = []
    try:
        grades = await get_grades(course_ids)
    except MoodleAPIError as exc:
        return [], _section_warning("grades", exc)

    for grade in grades:
        raw_grade = grade.grade_raw
        if raw_grade is None:
            continue

        new_grades.append(
            DashboardGrade(
                name=grade.name,
                course=grade.coursename or "",
                grade=raw_grade,
            )
        )
    return new_grades[:10], None
