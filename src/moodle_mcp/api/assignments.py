"""Assignment tool implementations."""

from __future__ import annotations

from moodle_mcp.api._helpers import get_course_ids, limit_items, require_write_reason
from moodle_mcp.api.coercion import (
    as_int,
    as_object,
    as_optional_float,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import (
    Assignment,
    AssignmentFile,
    FeedbackGrade,
    JsonObject,
    SubmissionStatus,
    WriteReceipt,
)
from moodle_mcp.moodle import APIFunction, format_array_params, get_moodle_api_data


async def get_assignments(
    course_ids: list[int] | None = None,
    limit: int = 50,
) -> list[Assignment]:
    """Return assignments across courses, optionally filtered."""
    cids = await get_course_ids(course_ids)
    if not cids:
        return []

    data = await get_moodle_api_data(
        APIFunction.mod_assign_get_assignments,
        format_array_params("courseids", cids),
    )
    if not isinstance(data, dict):
        return []

    assignments: list[Assignment] = []
    for course in object_list(data.get("courses")):
        for assignment in object_list(course.get("assignments")):
            assignments.append(_format_assignment(course, assignment))
    return limit_items(assignments, limit)


async def get_assignment_details(assignmentid: int) -> Assignment | None:
    """Return full details for a single assignment."""
    assignments = await get_assignments()
    return next((assignment for assignment in assignments if assignment.id == assignmentid), None)


async def get_assignment_files(assignmentid: int) -> list[AssignmentFile]:
    """Return attached files for an assignment."""
    cids = await get_course_ids()
    if not cids:
        return []

    data = await get_moodle_api_data(
        APIFunction.mod_assign_get_assignments,
        format_array_params("courseids", cids),
    )
    if not isinstance(data, dict):
        return []

    for course in object_list(data.get("courses")):
        for assignment in object_list(course.get("assignments")):
            if as_int(assignment.get("id")) != assignmentid:
                continue

            return _format_assignment_files(assignment)
    return []


async def submit_assignment(
    assignmentid: int,
    text: str | None = None,
    draft: bool = False,
    dry_run: bool = True,
    reason: str | None = None,
) -> WriteReceipt:
    """Save an assignment submission, and submit it for grading unless draft is True.

    With draft=False this saves the online text and then finalizes the submission for
    grading (mod_assign_submit_for_grading). With draft=True it only saves the online
    text and leaves the submission editable.
    """
    final_function = (
        APIFunction.mod_assign_save_submission
        if draft
        else APIFunction.mod_assign_submit_for_grading
    )
    if dry_run:
        intent = (
            "Save online text as a draft submission."
            if draft
            else "Save online text and submit this assignment for grading."
        )
        return WriteReceipt(
            dry_run=True,
            action="submit_assignment",
            target_type="assignment",
            target_id=assignmentid,
            would_change=[intent],
            warnings=["Dry run only. Pass dry_run=False with a reason to submit."],
            moodle_function=final_function.value,
        )

    require_write_reason(reason)

    save_params: dict[str, str] = {"assignmentid": str(assignmentid)}
    if text is not None:
        save_params["onlinetext"] = text
    await get_moodle_api_data(APIFunction.mod_assign_save_submission, save_params)

    if draft:
        return WriteReceipt(
            dry_run=False,
            action="submit_assignment",
            target_type="assignment",
            target_id=assignmentid,
            reason=reason,
            changed=["Saved assignment submission draft."],
            moodle_function=APIFunction.mod_assign_save_submission.value,
        )

    await get_moodle_api_data(
        APIFunction.mod_assign_submit_for_grading,
        {"assignmentid": str(assignmentid), "acceptsubmissionstatement": "1"},
    )
    return WriteReceipt(
        dry_run=False,
        action="submit_assignment",
        target_type="assignment",
        target_id=assignmentid,
        reason=reason,
        changed=["Saved online text and submitted the assignment for grading."],
        moodle_function=APIFunction.mod_assign_submit_for_grading.value,
    )


async def check_submission(assignmentid: int) -> SubmissionStatus:
    """Return submission status for an assignment."""
    data = await get_moodle_api_data(
        APIFunction.mod_assign_get_submission_status,
        {"assignid": str(assignmentid)},
    )
    data_object = data if isinstance(data, dict) else {}
    last = as_object(data_object.get("lastattempt"))
    submission = as_object(last.get("submission"))
    grade = as_object(as_object(data_object.get("feedback")).get("grade"))

    return SubmissionStatus(
        status=as_str(submission.get("status"), "noattempt"),
        timemodified=as_optional_int(submission.get("timemodified")),
        attemptnumber=as_optional_int(submission.get("attemptnumber")),
        gradingstatus="graded" if grade.get("grade") is not None else "notgraded",
    )


async def get_feedback(assignmentid: int) -> FeedbackGrade:
    """Return grade and feedback for a submitted assignment."""
    data = await get_moodle_api_data(
        APIFunction.mod_assign_get_submission_status,
        {"assignid": str(assignmentid)},
    )
    if not isinstance(data, dict):
        return FeedbackGrade(
            grade=None,
            maxgrade=None,
            feedback_text=None,
            timemodified=None,
            grader=None,
        )

    feedback_raw = as_object(data.get("feedback"))
    grade_raw = as_object(feedback_raw.get("grade"))
    grade_for_display = as_object(grade_raw.get("gradefordisplay"))
    grader = as_object(grade_raw.get("grader"))

    maxgrade = as_optional_float(grade_for_display.get("grade"))
    if maxgrade is None:
        maxgrade = as_optional_float(grade_raw.get("grade"))

    return FeedbackGrade(
        grade=as_optional_float(grade_raw.get("grade")),
        maxgrade=maxgrade,
        feedback_text=_extract_feedback_text(feedback_raw),
        timemodified=as_optional_int(grade_raw.get("timemodified")),
        grader=as_optional_str(grader.get("fullname")),
    )


def _format_assignment(course: JsonObject, assignment: JsonObject) -> Assignment:
    return Assignment(
        id=as_int(assignment.get("id")),
        cmid=as_int(assignment.get("cmid")),
        course=as_int(course.get("id")),
        name=as_str(assignment.get("name")),
        duedate=as_optional_int(assignment.get("duedate")),
        cutoffdate=as_optional_int(assignment.get("cutoffdate")),
        allowsubmissionsfromdate=as_optional_int(assignment.get("allowsubmissionsfromdate")),
        grade=as_optional_int(assignment.get("grade")),
        timemodified=as_optional_int(assignment.get("timemodified")),
        intro=as_optional_str(assignment.get("intro")),
        introformat=as_int(assignment.get("introformat"), 1),
        coursemodule=as_optional_int(assignment.get("coursemodule")),
    )


def _format_assignment_files(assignment: JsonObject) -> list[AssignmentFile]:
    return [
        AssignmentFile(
            filename=as_str(introfile.get("filename")),
            filepath=as_optional_str(introfile.get("filepath")),
            filesize=as_int(introfile.get("filesize")),
            mimetype=as_optional_str(introfile.get("mimetype")),
            fileurl=as_optional_str(introfile.get("fileurl")),
            timemodified=as_optional_int(introfile.get("timemodified")),
        )
        for introfile in object_list(assignment.get("introfiles"))
    ]


def _extract_feedback_text(feedback_raw: JsonObject) -> str | None:
    """Extract feedback text from plugins data."""
    for plugin in object_list(feedback_raw.get("plugins")):
        for filearea in object_list(plugin.get("fileareas")):
            for file_ in object_list(filearea.get("files")):
                filename = as_str(file_.get("filename"))
                if filename.endswith(".html"):
                    return as_optional_str(file_.get("filecontent"))

        for editor in object_list(plugin.get("editorfields")):
            return as_optional_str(editor.get("text"))
    return None
