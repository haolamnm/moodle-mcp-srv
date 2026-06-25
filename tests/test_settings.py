from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from moodle_mcp.config import Settings

if TYPE_CHECKING:
    from pathlib import Path


def test_settings_loads_os_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MOODLE_API_URL", "https://moodle.test/rest.php")
    monkeypatch.setenv("MOODLE_API_TOKEN", "secret")

    settings = Settings()
    settings.validate()

    assert settings.api_url == "https://moodle.test/rest.php"
    assert settings.api_token == "secret"


def test_settings_loads_dotenv_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MOODLE_API_URL", raising=False)
    monkeypatch.delenv("MOODLE_API_TOKEN", raising=False)
    tmp_path.joinpath(".env").write_text(
        "MOODLE_API_URL=https://dotenv.test/rest.php\nMOODLE_API_TOKEN=dotenv-token\n",
        encoding="utf-8",
    )

    settings = Settings()
    settings.validate()

    assert settings.api_url == "https://dotenv.test/rest.php"
    assert settings.api_token == "dotenv-token"


def test_settings_os_environment_overrides_dotenv_files(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    tmp_path.joinpath(".env").write_text(
        "MOODLE_API_URL=https://dotenv.test/rest.php\nMOODLE_API_TOKEN=dotenv-token\n",
        encoding="utf-8",
    )
    tmp_path.joinpath(".env.local").write_text(
        "MOODLE_API_URL=https://local-dotenv.test/rest.php\nMOODLE_API_TOKEN=local-dotenv-token\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("MOODLE_API_URL", "https://os-env.test/rest.php")
    monkeypatch.setenv("MOODLE_API_TOKEN", "os-env-token")

    settings = Settings()
    settings.validate()

    assert settings.api_url == "https://os-env.test/rest.php"
    assert settings.api_token == "os-env-token"


def test_settings_reports_missing_moodle_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MOODLE_API_URL", raising=False)
    monkeypatch.delenv("MOODLE_API_TOKEN", raising=False)

    settings = Settings()

    with pytest.raises(ValueError, match="MOODLE_API_URL is not set"):
        settings.validate()


def test_settings_reports_invalid_moodle_api_url(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MOODLE_API_URL", "not a url")
    monkeypatch.setenv("MOODLE_API_TOKEN", "secret")

    settings = Settings()

    with pytest.raises(ValueError, match="configuration invalid"):
        settings.validate()
