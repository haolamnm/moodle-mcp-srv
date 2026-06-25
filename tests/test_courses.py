from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import courses
from moodle_mcp.moodle import APIFunction

if TYPE_CHECKING:
    import pytest


def test_get_site_info_formats_moodle_site_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        assert function == APIFunction.core_webservice_get_site_info
        assert params is None
        return {
            "sitename": "Moodle Test",
            "siteurl": "https://moodle.test",
            "userid": "42",
            "username": "student",
            "firstname": "Ada",
            "lastname": "Lovelace",
            "fullname": "Ada Lovelace",
            "release": "5.0.1",
            "version": "2025041401",
        }

    monkeypatch.setattr(courses, "get_moodle_api_data", fake_get_moodle_api_data)

    site_info = asyncio.run(courses.get_site_info())

    assert site_info.model_dump() == {
        "sitename": "Moodle Test",
        "siteurl": "https://moodle.test",
        "userid": 42,
        "username": "student",
        "firstname": "Ada",
        "lastname": "Lovelace",
        "fullname": "Ada Lovelace",
        "release": "5.0.1",
        "version": "2025041401",
    }


def test_get_my_courses_formats_enrolled_courses(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_resolve_current_user_id() -> int:
        await asyncio.sleep(0)
        return 42

    async def fake_get_enrolled_courses(userid: int | None = None) -> list[dict[str, object]]:
        await asyncio.sleep(0)
        assert userid == 42
        return [
            {
                "id": "10",
                "fullname": "Algorithms",
                "shortname": "ALG",
                "category": "2",
                "summary": "Course summary",
                "startdate": "100",
                "enddate": None,
                "progress": "66.5",
            }
        ]

    monkeypatch.setattr(courses, "resolve_current_user_id", fake_resolve_current_user_id)
    monkeypatch.setattr(courses, "get_enrolled_courses", fake_get_enrolled_courses)

    result = asyncio.run(courses.get_my_courses())

    assert [course.model_dump() for course in result] == [
        {
            "id": 10,
            "fullname": "Algorithms",
            "shortname": "ALG",
            "category": 2,
            "summary": "Course summary",
            "startdate": 100,
            "enddate": None,
            "progress": 66.5,
        }
    ]


def test_get_course_content_formats_sections_and_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        assert function == APIFunction.core_course_get_contents
        captured_params.update(params or {})
        return [
            {
                "id": "1",
                "name": "Lecture",
                "summary": None,
                "modules": [
                    {
                        "id": "2",
                        "name": "Slides",
                        "modname": "resource",
                        "url": "https://moodle.test/mod/resource/view.php?id=2",
                    }
                ],
            }
        ]

    monkeypatch.setattr(courses, "get_moodle_api_data", fake_get_moodle_api_data)

    result = asyncio.run(courses.get_course_content(10))

    assert captured_params == {"courseid": "10"}
    assert [section.model_dump() for section in result] == [
        {
            "id": 1,
            "name": "Lecture",
            "summary": None,
            "modules": [
                {
                    "id": 2,
                    "name": "Slides",
                    "modname": "resource",
                    "url": "https://moodle.test/mod/resource/view.php?id=2",
                    "description": None,
                }
            ],
        }
    ]


def test_get_course_content_returns_empty_for_unexpected_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> dict[str, object]:
        await asyncio.sleep(0)
        _ = function, params
        return {"unexpected": True}

    monkeypatch.setattr(courses, "get_moodle_api_data", fake_get_moodle_api_data)

    assert asyncio.run(courses.get_course_content(10)) == []
