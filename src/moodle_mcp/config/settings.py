"""Environment-based configuration for the Moodle MCP server.

Validation is deferred to first use so the module can be imported
without env vars set (e.g. for CLI help or inspection).
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _EnvironmentSettings(BaseSettings):
    """Raw environment settings loaded by Pydantic."""

    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), extra="ignore")

    api_url: str = Field(default="", validation_alias="MOODLE_API_URL")
    api_token: str = Field(default="", validation_alias="MOODLE_API_TOKEN")


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

        env_settings = _EnvironmentSettings()
        errors: list[str] = []
        if not env_settings.api_url:
            errors.append("MOODLE_API_URL is not set")
        if not env_settings.api_token:
            errors.append("MOODLE_API_TOKEN is not set")

        if errors:
            msg = "; ".join(errors)
            raise ValueError(f"Moodle MCP configuration incomplete: {msg}")

        self.api_url = env_settings.api_url
        self.api_token = env_settings.api_token
        self._validated = True


settings = Settings()
