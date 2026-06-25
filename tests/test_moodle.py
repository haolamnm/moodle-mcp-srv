from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import httpx
from hypothesis import given, strategies as st
import pytest

from moodle_mcp.moodle import (
    APIFunction,
    MoodleAPIError,
    client,
    format_array_params,
    reset_current_user_cache,
    user,
)

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock


@given(
    key=st.from_regex(r"[A-Za-z_][A-Za-z0-9_]*", fullmatch=True),
    values=st.lists(st.one_of(st.integers(min_value=-1_000_000, max_value=1_000_000), st.text())),
)
def test_format_array_params_preserves_indexed_order(key: str, values: list[int | str]) -> None:
    params = format_array_params(key, values)

    assert params == {f"{key}[{index}]": str(value) for index, value in enumerate(values)}


@pytest.mark.asyncio
async def test_get_moodle_api_data_posts_form_data(
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(client, "_get_config", lambda: ("https://moodle.test/rest.php", "secret"))
    httpx_mock.add_response(method="POST", url="https://moodle.test/rest.php", json={"ok": True})

    result = await client.get_moodle_api_data(
        APIFunction.core_webservice_get_site_info,
        {"extra": "value"},
    )

    request = httpx_mock.get_request()
    assert result == {"ok": True}
    assert request is not None
    assert request.method == "POST"
    assert request.content == (
        b"wstoken=secret&wsfunction=core_webservice_get_site_info&"
        b"moodlewsrestformat=json&extra=value"
    )


@pytest.mark.asyncio
async def test_get_moodle_api_data_raises_http_error_after_retries(
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(client, "_get_config", lambda: ("https://moodle.test/rest.php", "secret"))
    for _ in range(3):
        httpx_mock.add_response(status_code=500, text="server error")

    with pytest.raises(MoodleAPIError) as exc_info:
        await client.get_moodle_api_data(APIFunction.core_webservice_get_site_info)

    assert exc_info.value.error_code == "http_error"


@pytest.mark.asyncio
async def test_get_moodle_api_data_raises_moodle_api_error(
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(client, "_get_config", lambda: ("https://moodle.test/rest.php", "secret"))
    httpx_mock.add_response(
        status_code=200,
        json={"errorcode": "invalidtoken", "message": "Invalid token"},
    )

    with pytest.raises(MoodleAPIError) as exc_info:
        await client.get_moodle_api_data(APIFunction.core_webservice_get_site_info)

    assert exc_info.value.error_code == "invalidtoken"


@pytest.mark.asyncio
async def test_get_moodle_api_data_raises_network_error(
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(client, "_get_config", lambda: ("https://moodle.test/rest.php", "secret"))
    httpx_mock.add_exception(httpx.RequestError("offline"))

    with pytest.raises(MoodleAPIError) as exc_info:
        await client.get_moodle_api_data(APIFunction.core_webservice_get_site_info)

    assert exc_info.value.error_code == "network_error"


def test_resolve_current_user_id_caches_user_id(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_current_user_cache()
    calls = 0

    async def fake_get_moodle_api_data(function: APIFunction) -> dict[str, object]:
        nonlocal calls
        await asyncio.sleep(0)
        calls += 1
        assert function == APIFunction.core_webservice_get_site_info
        return {"userid": "42"}

    monkeypatch.setattr(user, "get_moodle_api_data", fake_get_moodle_api_data)

    assert asyncio.run(user.resolve_current_user_id()) == 42
    assert asyncio.run(user.resolve_current_user_id()) == 42
    assert calls == 1


@pytest.mark.parametrize(
    ("response", "error_code"),
    [
        ({}, "no_userid"),
        ({"userid": "not-numeric"}, "invalid_userid"),
    ],
)
def test_resolve_current_user_id_reports_invalid_response(
    response: dict[str, object],
    error_code: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reset_current_user_cache()

    async def fake_get_moodle_api_data(function: APIFunction) -> dict[str, object]:
        await asyncio.sleep(0)
        _ = function
        return response

    monkeypatch.setattr(user, "get_moodle_api_data", fake_get_moodle_api_data)

    with pytest.raises(MoodleAPIError) as exc_info:
        asyncio.run(user.resolve_current_user_id())

    assert exc_info.value.error_code == error_code
