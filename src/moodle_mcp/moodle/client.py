"""Moodle REST transport client."""

from __future__ import annotations

from asyncio import AbstractEventLoop, get_running_loop
from typing import TYPE_CHECKING, cast
from weakref import WeakKeyDictionary

from aiolimiter import AsyncLimiter
import httpx
import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from moodle_mcp.config.settings import settings
from moodle_mcp.moodle.errors import MoodleAPIError

if TYPE_CHECKING:
    from moodle_mcp.models import JsonValue, MoodleResponse
    from moodle_mcp.moodle.functions import APIFunction

logger = structlog.get_logger(__name__)
_moodle_limiters: WeakKeyDictionary[AbstractEventLoop, AsyncLimiter] = WeakKeyDictionary()


class _TransientMoodleHTTPError(Exception):
    """Raised for retryable Moodle HTTP responses."""

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        super().__init__(f"Retryable Moodle HTTP {response.status_code}")


def _get_config() -> tuple[str, str]:
    """Validate settings and return Moodle API config."""
    settings.validate()
    return settings.api_url, settings.api_token


async def get_moodle_api_data(
    function: APIFunction,
    params: dict[str, str] | None = None,
) -> MoodleResponse:
    """Call a Moodle web service function and return the parsed JSON response."""
    api_url, api_token = _get_config()

    request_params: dict[str, str] = {
        "wstoken": api_token,
        "wsfunction": function.value,
        "moodlewsrestformat": "json",
    }
    if params:
        request_params.update(params)

    async with httpx.AsyncClient(timeout=30.0) as http_client:
        try:
            response = await _post_moodle_form(http_client, api_url, request_params)
        except httpx.RequestError as exc:
            logger.warning(
                "moodle_api_network_error",
                error=str(exc),
                wsfunction=function.value,
            )
            raise MoodleAPIError("network_error", str(exc), function.value) from exc
        except _TransientMoodleHTTPError as exc:
            response = exc.response

    if response.status_code != 200:
        logger.warning(
            "moodle_api_http_error",
            status_code=response.status_code,
            wsfunction=function.value,
        )
        raise MoodleAPIError(
            "http_error",
            f"HTTP {response.status_code}: {response.text[:300]}",
            function.value,
        )

    data = cast("MoodleResponse", response.json())
    if isinstance(data, dict) and "errorcode" in data:
        error_message = _str_value(data.get("message"), "Unknown Moodle API error")
        error_code = _str_value(data.get("errorcode"), "unknown")
        logger.warning(
            "moodle_api_error",
            error_code=error_code,
            wsfunction=function.value,
        )
        raise MoodleAPIError(error_code, error_message, function.value)

    return data


def _str_value(value: JsonValue | None, default: str) -> str:
    return value if isinstance(value, str) else default


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=5),
    retry=retry_if_exception_type(
        (httpx.ConnectError, httpx.TimeoutException, _TransientMoodleHTTPError)
    ),
    reraise=True,
)
async def _post_moodle_form(
    http_client: httpx.AsyncClient,
    api_url: str,
    request_params: dict[str, str],
) -> httpx.Response:
    """POST a Moodle form request with retry and rate-limit protection."""
    async with _get_moodle_limiter():
        response = await http_client.post(api_url, data=request_params)
    if response.status_code >= 500:
        raise _TransientMoodleHTTPError(response)
    return response


def _get_moodle_limiter() -> AsyncLimiter:
    loop = get_running_loop()
    limiter = _moodle_limiters.get(loop)
    if limiter is None:
        limiter = AsyncLimiter(30, 60)
        _moodle_limiters[loop] = limiter
    return limiter
