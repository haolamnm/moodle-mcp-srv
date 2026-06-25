"""Doctor diagnostics for Moodle setup."""

from __future__ import annotations

from moodle_mcp.api.courses import get_site_info
from moodle_mcp.api.features import build_capability_report, get_available_functions
from moodle_mcp.config.settings import settings
from moodle_mcp.models import DoctorCheck, DoctorReport, ServerCapabilityReport, SiteInfo
from moodle_mcp.moodle import MoodleAPIError


async def run_doctor(*, check_writes: bool = False) -> DoctorReport:
    """Validate config, token, Site Info, and expected Moodle functions."""
    checks: list[DoctorCheck] = []
    site_info: SiteInfo | None = None
    features: ServerCapabilityReport | None = None

    try:
        settings.validate()
    except ValueError as exc:
        checks.append(
            DoctorCheck(
                name="config",
                status="error",
                message=str(exc),
                action="Set MOODLE_API_URL and MOODLE_API_TOKEN, then rerun `moodle-mcp doctor`.",
            )
        )
        return DoctorReport(ok=False, site_info=None, checks=checks, features=None)

    checks.append(
        DoctorCheck(
            name="config",
            status="ok",
            message="MOODLE_API_URL and MOODLE_API_TOKEN are configured.",
        )
    )

    try:
        site_info = await get_site_info()
    except MoodleAPIError as exc:
        checks.append(
            DoctorCheck(
                name="site_info",
                status="error",
                message=f"Site Info failed: {exc.error_code}.",
                action=_moodle_error_action(exc),
            )
        )
        return DoctorReport(ok=False, site_info=None, checks=checks, features=None)

    checks.append(
        DoctorCheck(
            name="site_info",
            status="ok",
            message="Site Info returned authenticated Moodle metadata.",
        )
    )

    try:
        available_functions = await get_available_functions(refresh=True)
    except MoodleAPIError as exc:
        checks.append(
            DoctorCheck(
                name="functions",
                status="warning",
                message=f"Could not inspect Moodle Web Service Function Names: {exc.error_code}.",
                action=_moodle_error_action(exc),
            )
        )
        features = build_capability_report(None, include_writes=check_writes)
    else:
        features = build_capability_report(available_functions, include_writes=check_writes)
        checks.append(_functions_check(features, check_writes=check_writes))

    ok = all(check.status != "error" for check in checks)
    return DoctorReport(
        ok=ok,
        site_info=site_info,
        checks=checks,
        features=features,
        check_writes=check_writes,
    )


def _functions_check(
    features: ServerCapabilityReport,
    *,
    check_writes: bool,
) -> DoctorCheck:
    if not features.available_functions_known:
        return DoctorCheck(
            name="functions",
            status="warning",
            message="Site Info did not expose Moodle Web Service Function Names.",
            action="Run a read-only smoke test, or ask a Moodle admin to confirm the external service functions.",
        )

    missing = sorted(
        {function for feature in features.features for function in feature.missing_functions}
    )
    if missing:
        return DoctorCheck(
            name="functions",
            status="warning",
            message=(
                f"{len(features.expected_functions) - len(missing)}/"
                f"{len(features.expected_functions)} expected functions are available."
            ),
            action="Ask a Moodle admin to add the missing function(s) to the external service.",
        )

    scope = "read/write" if check_writes else "read-only"
    return DoctorCheck(
        name="functions",
        status="ok",
        message=f"All expected {scope} Moodle Web Service Function Names are available.",
    )


def _moodle_error_action(exc: MoodleAPIError) -> str:
    if exc.error_code == "invalidtoken":
        return "Create or refresh the Moodle Web Service token for this user."
    if exc.error_code == "accessexception":
        return "Ask a Moodle admin to enable the Web Service and token permissions."
    if exc.error_code == "invalidrecord":
        return "Ask a Moodle admin to add the missing function to the external service."
    return "Check Moodle Web Services, REST protocol, token setup, and the configured API URL."
