"""Grade and completion tool implementations."""

from __future__ import annotations

from moodle_mcp.api._helpers import (
    get_course_ids,
    get_enrolled_courses,
    limit_items,
    require_write_reason,
)
from moodle_mcp.api.coercion import (
    as_int,
    as_object,
    as_optional_float,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import CompletionActivity, GradeItem, WriteReceipt
from moodle_mcp.moodle import APIFunction, get_moodle_api_data, resolve_current_user_id


async def get_grades(
    course_ids: list[int] | None = None,
    limit: int = 100,
) -> list[GradeItem]:
    """Return grade items across courses."""
    cids = await get_course_ids(course_ids)
    if not cids:
        return []

    grades: list[GradeItem] = []
    userid = await resolve_current_user_id()
    courses_raw = await get_enrolled_courses()

    for cid in cids:
        data = await get_moodle_api_data(
            APIFunction.gradereport_user_get_grade_items,
            {"courseid": str(cid), "userid": str(userid)},
        )
        if not isinstance(data, dict):
            continue

        course_name = next(
            (
                as_str(course.get("fullname"))
                for course in courses_raw
                if as_int(course.get("id")) == cid
            ),
            "",
        )
        for item in object_list(data.get("gradeitems")):
            feedback = as_object(item.get("feedback"))
            grades.append(
                GradeItem(
                    id=as_int(item.get("id")),
                    name=as_str(item.get("itemname")),
                    coursename=course_name,
                    courseid=cid,
                    grade_raw=as_optional_float(item.get("graderaw")),
                    grade_percent=as_optional_str(item.get("percentageformatted")),
                    grade_letter=as_optional_str(item.get("lettergradeformatted")),
                    range_min=as_optional_float(item.get("rangemin")),
                    range_max=as_optional_float(item.get("rangemax")),
                    feedback=as_optional_str(feedback.get("text")),
                )
            )
    return limit_items(grades, limit)


async def mark_activity_complete(
    cmid: int,
    completed: bool = True,
    dry_run: bool = True,
    reason: str | None = None,
) -> WriteReceipt:
    """Manually set the Activity Completion state for a course module."""
    function = APIFunction.core_completion_update_activity_completion_status_manually
    if dry_run:
        return WriteReceipt(
            dry_run=True,
            action="mark_activity_complete",
            target_type="activity",
            target_id=cmid,
            would_change=[
                "Mark this activity complete." if completed else "Mark this activity incomplete."
            ],
            warnings=["Dry run only. Pass dry_run=False with a reason to update completion."],
            moodle_function=function.value,
        )

    require_write_reason(reason)
    await get_moodle_api_data(
        function,
        {"cmid": str(cmid), "completed": "1" if completed else "0"},
    )
    state = "complete" if completed else "incomplete"
    return WriteReceipt(
        dry_run=False,
        action="mark_activity_complete",
        target_type="activity",
        target_id=cmid,
        reason=reason,
        changed=[f"Marked activity {cmid} {state}."],
        moodle_function=function.value,
    )


async def get_course_progress(courseid: int, limit: int = 100) -> list[CompletionActivity]:
    """Return completion status for all activities in a course."""
    userid = await resolve_current_user_id()
    data = await get_moodle_api_data(
        APIFunction.core_completion_get_activities_completion_status,
        {"courseid": str(courseid), "userid": str(userid)},
    )
    if not isinstance(data, dict):
        return []

    activities: list[CompletionActivity] = []
    for item in object_list(data.get("statuses")):
        state = as_int(item.get("state"))
        activities.append(
            CompletionActivity(
                id=as_int(item.get("cmid")),
                name=as_str(item.get("activityname")),
                modname=as_str(item.get("modname")),
                completionstatus="complete" if state == 1 else "incomplete",
                timecompleted=as_optional_int(item.get("timecompleted")),
            )
        )
    return limit_items(activities, limit)
