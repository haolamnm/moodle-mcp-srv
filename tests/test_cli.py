from __future__ import annotations

import asyncio
import importlib
import json
from typing import TYPE_CHECKING

from typer.testing import CliRunner

from moodle_mcp.cli import main
from moodle_mcp.cli.app import app as typer_app
from moodle_mcp.cli.commands import diagnostics
from moodle_mcp.models import DoctorCheck, DoctorReport, ServerCapabilityReport, SiteInfo

if TYPE_CHECKING:
    import pytest

runner = CliRunner()
cli_app_module = importlib.import_module("moodle_mcp.cli.app")
serve_command_module = importlib.import_module("moodle_mcp.cli.commands.serve")


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
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        assert check_writes is True
        return _doctor_report()

    monkeypatch.setattr(diagnostics.api, "run_doctor", fake_run_doctor)

    result = runner.invoke(typer_app, ["doctor", "--json", "--check-writes"])

    assert result.exit_code == 0
    assert '"ok":true' in result.output


def test_main_runs_doctor_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        assert check_writes is False
        return _doctor_report()

    monkeypatch.setattr(diagnostics.api, "run_doctor", fake_run_doctor)

    result = runner.invoke(typer_app, ["doctor"])

    assert result.exit_code == 0
    assert "Moodle MCP Doctor" in result.output
    assert "Mock Moodle" in result.output
    assert "Write checks: skipped" in result.output


def test_main_exits_nonzero_for_failed_doctor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_run_doctor(*, check_writes: bool = False) -> DoctorReport:
        await asyncio.sleep(0)
        _ = check_writes
        return _doctor_report(ok=False)

    monkeypatch.setattr(diagnostics.api, "run_doctor", fake_run_doctor)

    result = runner.invoke(typer_app, ["doctor"])

    assert result.exit_code == 1
    assert "Missing config" in result.output


def test_root_runs_http_server(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_serve_mcp_server(*, http: bool, host: str, port: int) -> None:
        calls.append({"http": http, "host": host, "port": port})

    monkeypatch.setattr(cli_app_module, "serve_mcp_server", fake_serve_mcp_server)

    result = runner.invoke(typer_app, ["--http", "--host", "0.0.0.0", "--port", "9000"])

    assert result.exit_code == 0
    assert calls == [{"http": True, "host": "0.0.0.0", "port": 9000}]


def test_serve_command_runs_http_server(monkeypatch: pytest.MonkeyPatch) -> None:
    server = _FakeServer()

    def fake_create_server() -> _FakeServer:
        return server

    monkeypatch.setattr(serve_command_module, "create_server", fake_create_server)

    result = runner.invoke(typer_app, ["serve", "--http", "--host", "0.0.0.0", "--port", "9000"])

    assert result.exit_code == 0
    assert server.calls == [{"transport": "http", "host": "0.0.0.0", "port": 9000}]


def test_serve_command_runs_stdio_server(monkeypatch: pytest.MonkeyPatch) -> None:
    server = _FakeServer()

    def fake_create_server() -> _FakeServer:
        return server

    monkeypatch.setattr(serve_command_module, "create_server", fake_create_server)

    result = runner.invoke(typer_app, ["serve"])

    assert result.exit_code == 0
    assert server.calls == [{}]


def test_ping_command_reports_site_info(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_get_site_info() -> SiteInfo:
        await asyncio.sleep(0)
        site_info = _doctor_report().site_info
        assert site_info is not None
        return site_info

    monkeypatch.setattr(diagnostics.api, "get_site_info", fake_get_site_info)

    result = runner.invoke(typer_app, ["ping"])

    assert result.exit_code == 0
    assert "OK: Mock Moodle" in result.output


def test_inspect_command_reports_mcp_surface() -> None:
    result = runner.invoke(typer_app, ["inspect", "--json"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "get_site_info" in data["tools"]
    assert "moodle://site/features" in data["resources"]


def test_main_invokes_typer_app(monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fake_app() -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(cli_app_module, "app", fake_app)

    main()

    assert called is True
