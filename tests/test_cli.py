from __future__ import annotations

import asyncio
import sys

import pytest

from moodle_mcp import cli
from moodle_mcp.models import DoctorCheck, DoctorReport, ServerCapabilityReport, SiteInfo


class _FakeServer:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def run(self, **kwargs: object) -> None:
        self.calls.append(kwargs)


def _doctor_report(*, ok: bool = True) -> DoctorReport:
    return DoctorReport(
        ok=ok,
        site_info=SiteInfo(
            sitename="Mock Moodle",
            siteurl="https://moodle.test",
            userid=42,
            username=None,
            firstname=None,
            lastname=None,
            fullname=None,
            release="5.0.1",
            version="2025041401",
        ),
        checks=[
            DoctorCheck(
                name="config",
                status="ok" if ok else "error",
                message="Configured." if ok else "Missing config.",
                action=None if ok else "Set environment variables.",
            )
        ],
        features=ServerCapabilityReport(
            available_functions_known=True,
            expected_functions=["core_webservice_get_site_info"],
            available_functions=["core_webservice_get_site_info"],
            features=[],
        ),
    )


def test_main_runs_doctor_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        assert check_writes is True
        return _doctor_report()

    monkeypatch.setattr(sys, "argv", ["moodle-mcp", "doctor", "--json", "--check-writes"])
    monkeypatch.setattr(cli.api, "run_doctor", fake_run_doctor)

    cli.main()

    assert '"ok":true' in capsys.readouterr().out


def test_main_runs_doctor_text(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        assert check_writes is False
        return _doctor_report()

    monkeypatch.setattr(sys, "argv", ["moodle-mcp", "doctor"])
    monkeypatch.setattr(cli.api, "run_doctor", fake_run_doctor)

    cli.main()

    text = capsys.readouterr().out
    assert "Moodle MCP Doctor" in text
    assert "Mock Moodle" in text
    assert "Write checks: skipped" in text


def test_main_exits_nonzero_for_failed_doctor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        _ = check_writes
        return _doctor_report(ok=False)

    monkeypatch.setattr(sys, "argv", ["moodle-mcp", "doctor"])
    monkeypatch.setattr(cli.api, "run_doctor", fake_run_doctor)

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 1


def test_main_runs_http_server(monkeypatch: pytest.MonkeyPatch) -> None:
    server = _FakeServer()

    def fake_create_server() -> _FakeServer:
        return server

    monkeypatch.setattr(
        sys, "argv", ["moodle-mcp", "--http", "--host", "0.0.0.0", "--port", "9000"]
    )
    monkeypatch.setattr(cli, "create_server", fake_create_server)

    cli.main()

    assert server.calls == [{"transport": "http", "host": "0.0.0.0", "port": 9000}]


def test_main_runs_stdio_server(monkeypatch: pytest.MonkeyPatch) -> None:
    server = _FakeServer()

    def fake_create_server() -> _FakeServer:
        return server

    monkeypatch.setattr(sys, "argv", ["moodle-mcp"])
    monkeypatch.setattr(cli, "create_server", fake_create_server)

    cli.main()

    assert server.calls == [{}]
