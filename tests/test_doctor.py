from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from moodle_mcp.api import doctor
from moodle_mcp.models import SiteInfo
from moodle_mcp.moodle import APIFunction, MoodleAPIError

if TYPE_CHECKING:
    import pytest


class _FakeSettings:
    @staticmethod
    def validate() -> None:
        return None


class _MissingSettings:
    @staticmethod
    def validate() -> None:
        raise ValueError("Moodle MCP configuration incomplete: MOODLE_API_URL is not set")


def _site_info() -> SiteInfo:
    return SiteInfo(
        sitename="Mock Moodle",
        siteurl="https://moodle.test",
        userid=42,
        username="student",
        firstname="Ada",
        lastname="Lovelace",
        fullname="Ada Lovelace",
        release="5.0.1",
        version="2025041401",
    )


def test_run_doctor_reports_missing_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(doctor, "settings", _MissingSettings())

    report = asyncio.run(doctor.run_doctor())

    assert report.ok is False
    assert report.checks[0].name == "config"
    assert report.checks[0].status == "error"
    assert report.features is None


def test_run_doctor_reports_available_read_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_site_info() -> SiteInfo:
        await asyncio.sleep(0)
        return _site_info()

    async def fake_get_available_functions(*, refresh: bool = False) -> frozenset[str]:
        await asyncio.sleep(0)
        assert refresh is True
        return frozenset(function.value for function in APIFunction)

    monkeypatch.setattr(doctor, "settings", _FakeSettings())
    monkeypatch.setattr(doctor, "get_site_info", fake_get_site_info)
    monkeypatch.setattr(doctor, "get_available_functions", fake_get_available_functions)

    report = asyncio.run(doctor.run_doctor(check_writes=True))

    assert report.ok is True
    assert [check.status for check in report.checks] == ["ok", "ok", "ok"]
    assert report.features is not None
    assert all(feature.status == "available" for feature in report.features.features)


def test_run_doctor_warns_for_missing_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_site_info() -> SiteInfo:
        await asyncio.sleep(0)
        return _site_info()

    async def fake_get_available_functions(*, refresh: bool = False) -> frozenset[str]:
        await asyncio.sleep(0)
        _ = refresh
        return frozenset({APIFunction.core_webservice_get_site_info.value})

    monkeypatch.setattr(doctor, "settings", _FakeSettings())
    monkeypatch.setattr(doctor, "get_site_info", fake_get_site_info)
    monkeypatch.setattr(doctor, "get_available_functions", fake_get_available_functions)

    report = asyncio.run(doctor.run_doctor())

    assert report.ok is True
    assert report.checks[-1].status == "warning"
    assert report.features is not None
    assert any(feature.missing_functions for feature in report.features.features)


def test_run_doctor_reports_site_info_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_site_info() -> SiteInfo:
        await asyncio.sleep(0)
        raise MoodleAPIError("invalidtoken", "Invalid token", "core_webservice_get_site_info")

    monkeypatch.setattr(doctor, "settings", _FakeSettings())
    monkeypatch.setattr(doctor, "get_site_info", fake_get_site_info)

    report = asyncio.run(doctor.run_doctor())

    assert report.ok is False
    assert report.checks[-1].name == "site_info"
    assert report.checks[-1].action is not None
    assert "token" in report.checks[-1].action
