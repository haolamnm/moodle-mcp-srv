from __future__ import annotations

import asyncio

import pytest

from moodle_mcp.api import assignments
from moodle_mcp.moodle import APIFunction


def test_get_assignments_formats_assignments(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        assert course_ids == [10]
        return [10]

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_assign_get_assignments
        assert params == {"courseids[0]": "10"}
        return {
            "courses": [
                {
                    "id": "10",
                    "assignments": [
                        {
                            "id": "99",
                            "cmid": "88",
                            "name": "Assignment 1",
                            "duedate": "100",
                            "cutoffdate": None,
                            "allowsubmissionsfromdate": "50",
                            "grade": "10",
                            "timemodified": "70",
                            "intro": "<p>Brief</p>",
                            "introformat": "1",
                            "coursemodule": "88",
                        }
                    ],
                }
            ]
        }

    monkeypatch.setattr(assignments, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(assignments.get_assignments([10]))

    assert [assignment.model_dump() for assignment in result] == [
        {
            "id": 99,
            "cmid": 88,
            "course": 10,
            "name": "Assignment 1",
            "duedate": 100,
            "cutoffdate": None,
            "allowsubmissionsfromdate": 50,
            "grade": 10,
            "timemodified": 70,
            "intro": "<p>Brief</p>",
            "introformat": 1,
            "coursemodule": 88,
        }
    ]


def test_get_assignments_returns_empty_without_courses(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_course_ids(course_ids: list[int] | None = None) -> list[int]:
        await asyncio.sleep(0)
        _ = course_ids
        return []

    monkeypatch.setattr(assignments, "get_course_ids", fake_get_course_ids)

    assert asyncio.run(assignments.get_assignments()) == []


def test_get_assignment_details_finds_matching_assignment(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_assignments(
        course_ids: list[int] | None = None,
        limit: int = 50,
    ) -> list[assignments.Assignment]:
        await asyncio.sleep(0)
        _ = course_ids, limit
        return [
            assignments.Assignment(
                id=1,
                cmid=10,
                course=20,
                name="Assignment 1",
                duedate=None,
                cutoffdate=None,
                allowsubmissionsfromdate=None,
                grade=None,
                timemodified=None,
                intro=None,
                introformat=1,
                coursemodule=None,
            )
        ]

    monkeypatch.setattr(assignments, "get_assignments", fake_get_assignments)

    assert asyncio.run(assignments.get_assignment_details(1)) is not None
    assert asyncio.run(assignments.get_assignment_details(2)) is None


def test_get_assignment_files_uses_enrolled_course_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, str] = {}

    async def fake_get_course_ids() -> list[int]:
        await asyncio.sleep(0)
        return [10, 20]

    async def fake_get_moodle_api_data(
        function: object,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        _ = function
        captured_params.update(params or {})
        return {
            "courses": [
                {
                    "id": 10,
                    "assignments": [
                        {
                            "id": 99,
                            "introfiles": [
                                {
                                    "filename": "brief.pdf",
                                    "filepath": "/",
                                    "filesize": 123,
                                    "mimetype": "application/pdf",
                                    "fileurl": "https://moodle.test/brief.pdf",
                                    "timemodified": 456,
                                }
                            ],
                        }
                    ],
                }
            ]
        }

    monkeypatch.setattr(assignments, "get_course_ids", fake_get_course_ids)
    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    files = asyncio.run(assignments.get_assignment_files(99))

    assert captured_params == {"courseids[0]": "10", "courseids[1]": "20"}
    assert [file.model_dump() for file in files] == [
        {
            "filename": "brief.pdf",
            "filepath": "/",
            "filesize": 123,
            "mimetype": "application/pdf",
            "fileurl": "https://moodle.test/brief.pdf",
            "timemodified": 456,
        }
    ]


def test_check_submission_uses_assignid_param(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_function: APIFunction | None = None
    captured_params: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        nonlocal captured_function
        await asyncio.sleep(0)
        captured_function = function
        captured_params.update(params or {})
        return {
            "lastattempt": {
                "submission": {
                    "status": "submitted",
                    "timemodified": 123,
                    "attemptnumber": 1,
                }
            },
            "feedback": {"grade": {"grade": 9}},
        }

    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    status = asyncio.run(assignments.check_submission(99))

    assert captured_function == APIFunction.mod_assign_get_submission_status
    assert captured_params == {"assignid": "99"}
    assert status.status == "submitted"
    assert status.gradingstatus == "graded"


def test_get_feedback_uses_assignid_param(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.mod_assign_get_submission_status
        captured_params.update(params or {})
        return {
            "feedback": {
                "grade": {
                    "grade": 8.5,
                    "timemodified": 456,
                    "grader": {"fullname": "Teacher"},
                },
                "plugins": [{"editorfields": [{"text": "Good work"}]}],
            }
        }

    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    feedback = asyncio.run(assignments.get_feedback(99))

    assert captured_params == {"assignid": "99"}
    assert feedback.grade == pytest.approx(8.5)
    assert feedback.feedback_text == "Good work"


def test_submit_assignment_defaults_to_dry_run() -> None:
    receipt = asyncio.run(assignments.submit_assignment(99, "Done"))

    assert receipt.dry_run is True
    assert receipt.action == "submit_assignment"
    assert receipt.target_id == 99


def test_submit_assignment_requires_reason_when_not_dry_run() -> None:
    with pytest.raises(ValueError, match="reason"):
        asyncio.run(assignments.submit_assignment(99, "Done", dry_run=False))


def test_submit_assignment_draft_only_saves(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[APIFunction, dict[str, str] | None]] = []

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        calls.append((function, params))
        return []

    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    receipt = asyncio.run(
        assignments.submit_assignment(
            99, "Done", draft=True, dry_run=False, reason="User confirmed"
        )
    )

    assert calls == [
        (APIFunction.mod_assign_save_submission, {"assignmentid": "99", "onlinetext": "Done"})
    ]
    assert receipt.changed == ["Saved assignment submission draft."]
    assert receipt.moodle_function == APIFunction.mod_assign_save_submission.value


def test_submit_assignment_submits_for_grading(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[APIFunction, dict[str, str] | None]] = []

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        calls.append((function, params))
        return []

    monkeypatch.setattr(assignments, "get_moodle_api_data", fake_get_moodle_api_data)

    receipt = asyncio.run(
        assignments.submit_assignment(99, "Done", dry_run=False, reason="User confirmed")
    )

    assert calls == [
        (APIFunction.mod_assign_save_submission, {"assignmentid": "99", "onlinetext": "Done"}),
        (
            APIFunction.mod_assign_submit_for_grading,
            {"assignmentid": "99", "acceptsubmissionstatement": "1"},
        ),
    ]
    assert receipt.changed == ["Saved online text and submitted the assignment for grading."]
    assert receipt.moodle_function == APIFunction.mod_assign_submit_for_grading.value
