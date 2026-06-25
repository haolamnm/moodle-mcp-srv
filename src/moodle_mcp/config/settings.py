"""Environment-based configuration for the Moodle MCP server.

Validation is deferred to first use so the module can be imported
without env vars set (e.g. for CLI help or inspection).
"""

from __future__ import annotations

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from moodle_mcp.models.strings import MoodleApiToken, MoodleApiUrl  # noqa: TC001


class _EnvironmentSettings(BaseSettings):
    """Raw environment settings loaded by Pydantic."""

    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), extra="ignore")

    api_url: MoodleApiUrl | None = Field(default=None, validation_alias="MOODLE_API_URL")
    api_token: MoodleApiToken | None = Field(default=None, validation_alias="MOODLE_API_TOKEN")


class Settings:
    """Load and validate Moodle API configuration from environment variables."""

    def __init__(self) -> None:
        self._validated = False
        self.api_url: str = ""
        self.api_token: str = ""

    def validate(self) -> None:
        """Read and validate env vars. Called on first access."""
        if self._validated:
            return

        try:
            env_settings = _EnvironmentSettings()
        except ValidationError as exc:
            raise ValueError(f"Moodle MCP configuration invalid: {exc}") from exc

        api_url = env_settings.api_url
        api_token = env_settings.api_token

        errors: list[str] = []
        if api_url is None:
            errors.append("MOODLE_API_URL is not set")
        if api_token is None:
            errors.append("MOODLE_API_TOKEN is not set")

        if errors:
            msg = "; ".join(errors)
            raise ValueError(f"Moodle MCP configuration incomplete: {msg}")

        if api_url is None or api_token is None:
            raise AssertionError("Settings validation failed to narrow required values.")

        self.api_url = str(api_url)
        self.api_token = api_token.get_secret_value()
        self._validated = True


settings = Settings()
