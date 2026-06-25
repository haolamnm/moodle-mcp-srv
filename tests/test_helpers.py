from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import _helpers  # noqa: PLC2701
from moodle_mcp.moodle import APIFunction

if TYPE_CHECKING:
    import pytest


def test_get_enrolled_courses_fetches_for_user(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_params: dict[str, str] = {}

    async def fake_get_moodle_api_data(
        function: APIFunction,
        params: dict[str, str] | None = None,
    ) -> list[object]:
        await asyncio.sleep(0)
        assert function == APIFunction.core_enrol_get_users_courses
        captured_params.update(params or {})
        return [{"id": 10}, "ignored"]

    monkeypatch.setattr(_helpers, "get_moodle_api_data", fake_get_moodle_api_data)

    courses = asyncio.run(_helpers.get_enrolled_courses(42))

    assert captured_params == {"userid": "42"}
    assert courses == [{"id": 10}]


def test_get_course_ids_defaults_to_enrolled_course_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_enrolled_courses(userid: int | None = None) -> list[dict[str, object]]:
        await asyncio.sleep(0)
        assert userid is None
        return [{"id": "10"}, {"id": None}, {"id": 20}]

    monkeypatch.setattr(_helpers, "get_enrolled_courses", fake_get_enrolled_courses)

    assert asyncio.run(_helpers.get_course_ids()) == [10, 20]


def test_get_course_ids_preserves_explicit_filter() -> None:
    assert asyncio.run(_helpers.get_course_ids([3, 4])) == [3, 4]


def test_limit_helpers_and_course_accessors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_helpers, "now_ts", lambda: 1_000)

    assert _helpers.days_remaining(1_000) == 0
    assert _helpers.days_remaining(1_000 + _helpers.DAYS_SECONDS * 2) == 2
    assert _helpers.normalize_limit(0) == _helpers.DEFAULT_LIMIT
    assert _helpers.normalize_limit(500) == _helpers.MAX_LIMIT
    assert _helpers.limit_items([1, 2, 3], 2) == [1, 2]
    assert _helpers.course_name({"fullname": "Algorithms"}) == "Algorithms"
    assert not _helpers.course_name({"fullname": 10})
    assert _helpers.course_id({"id": "42"}) == 42


def test_require_write_reason_rejects_blank_reason() -> None:
    for blank in (None, "", "   "):
        raised = False
        try:
            _helpers.require_write_reason(blank)
        except ValueError:
            raised = True
        assert raised, f"expected ValueError for reason {blank!r}"


def test_require_write_reason_accepts_text() -> None:
    _helpers.require_write_reason("User confirmed")
