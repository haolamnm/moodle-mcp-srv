"""Moodle Feature registry and availability helpers."""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from moodle_mcp.api.coercion import as_optional_str, object_list
from moodle_mcp.models import FeatureAvailability, JsonObject, ServerCapabilityReport
from moodle_mcp.moodle import APIFunction, get_moodle_api_data

if TYPE_CHECKING:
    from collections.abc import Iterable


class MoodleFeature(StrEnum):
    """App-level capabilities backed by Moodle Web Service Function Names."""

    site_info = "site_info"
    courses = "courses"
    course_content = "course_content"
    calendar = "calendar"
    assignments = "assignments"
    assignment_submission = "assignment_submission"
    write_assignment = "write_assignment"
    submit_for_grading = "submit_for_grading"
    grades = "grades"
    progress = "progress"
    write_completion = "write_completion"
    write_calendar = "write_calendar"
    quizzes = "quizzes"
    quiz_attempts = "quiz_attempts"
    quiz_review = "quiz_review"
    forums = "forums"
    announcements = "announcements"
    write_forum = "write_forum"
    dashboard = "dashboard"


FEATURE_REQUIREMENTS: dict[MoodleFeature, tuple[APIFunction, ...]] = {
    MoodleFeature.site_info: (APIFunction.core_webservice_get_site_info,),
    MoodleFeature.courses: (
        APIFunction.core_webservice_get_site_info,
        APIFunction.core_enrol_get_users_courses,
    ),
    MoodleFeature.course_content: (APIFunction.core_course_get_contents,),
    MoodleFeature.calendar: (APIFunction.core_calendar_get_calendar_upcoming_view,),
    MoodleFeature.assignments: (APIFunction.mod_assign_get_assignments,),
    MoodleFeature.assignment_submission: (APIFunction.mod_assign_get_submission_status,),
    MoodleFeature.write_assignment: (APIFunction.mod_assign_save_submission,),
    MoodleFeature.submit_for_grading: (APIFunction.mod_assign_submit_for_grading,),
    MoodleFeature.grades: (APIFunction.gradereport_user_get_grade_items,),
    MoodleFeature.progress: (APIFunction.core_completion_get_activities_completion_status,),
    MoodleFeature.write_completion: (
        APIFunction.core_completion_update_activity_completion_status_manually,
    ),
    MoodleFeature.write_calendar: (APIFunction.core_calendar_create_calendar_events,),
    MoodleFeature.quizzes: (APIFunction.mod_quiz_get_quizzes_by_courses,),
    MoodleFeature.quiz_attempts: (
        APIFunction.core_webservice_get_site_info,
        APIFunction.mod_quiz_get_user_attempts,
    ),
    MoodleFeature.quiz_review: (APIFunction.mod_quiz_get_attempt_review,),
    MoodleFeature.forums: (
        APIFunction.mod_forum_get_forums_by_courses,
        APIFunction.mod_forum_get_forum_discussions,
    ),
    MoodleFeature.announcements: (
        APIFunction.mod_forum_get_forums_by_courses,
        APIFunction.mod_forum_get_forum_discussions,
    ),
    MoodleFeature.write_forum: (
        APIFunction.mod_forum_add_discussion_post,
        APIFunction.mod_forum_add_discussion,
    ),
    MoodleFeature.dashboard: (
        APIFunction.core_webservice_get_site_info,
        APIFunction.core_enrol_get_users_courses,
        APIFunction.mod_assign_get_assignments,
    ),
}

WRITE_FEATURES = frozenset(
    {
        MoodleFeature.write_assignment,
        MoodleFeature.submit_for_grading,
        MoodleFeature.write_forum,
        MoodleFeature.write_completion,
        MoodleFeature.write_calendar,
    }
)


class FailureKind(StrEnum):
    """How a Moodle call failed, used to choose the right guidance message."""

    missing_function = "missing_function"
    access_denied = "access_denied"
    unknown = "unknown"


_MISSING_FUNCTION_CODES = frozenset({"invalidrecord"})
_ACCESS_DENIED_CODES = frozenset(
    {
        "accessexception",
        "nopermissions",
        "required_capability_exception",
        "webservice_access_exception",
    }
)


def classify_failure(error_code: str) -> FailureKind:
    """Classify a Moodle error code into setup-vs-access-vs-unknown guidance."""
    if error_code in _MISSING_FUNCTION_CODES:
        return FailureKind.missing_function
    if error_code in _ACCESS_DENIED_CODES:
        return FailureKind.access_denied
    return FailureKind.unknown


def access_error_message(feature: MoodleFeature, error_code: str) -> str:
    """Return guidance for an Access Error: Moodle refused this request at call time.

    This is distinct from a missing Moodle Feature: the function may exist but your
    Moodle account or token cannot access it on this site. Moodle enforces this;
    moodle-mcp-srv does not authorize anything.
    """
    return (
        f"Moodle refused this request for '{feature.value}' (error: {error_code}). "
        "Your Moodle account may not have access to this on the current site, or the "
        "Web Service Function Name may not be authorized for your token. Moodle enforces "
        "this; moodle-mcp-srv does not. Run `moodle-mcp doctor` for setup guidance."
    )


_available_functions_loaded = False
_available_functions_cache: frozenset[str] | None = None


class UnavailableFeatureError(Exception):
    """Raised when a Moodle Feature is known to be unavailable."""

    def __init__(self, feature: MoodleFeature, missing_functions: list[str]) -> None:
        self.feature = feature
        self.missing_functions = missing_functions
        super().__init__(feature_unavailable_message(feature, missing_functions))


async def get_server_capabilities() -> ServerCapabilityReport:
    """Return Moodle Feature availability for the current token and site."""
    available_functions = await get_available_functions()
    return build_capability_report(available_functions)


async def ensure_feature_available(feature: MoodleFeature) -> None:
    """Raise if a Moodle Feature is known to be unavailable."""
    report = build_capability_report(await get_available_functions())
    availability = next(item for item in report.features if item.feature == feature.value)
    if availability.status != "missing_function":
        return

    raise UnavailableFeatureError(feature, availability.missing_functions)


def feature_unavailable_message(feature: MoodleFeature, missing_functions: list[str]) -> str:
    """Return an action-oriented message for missing function setup."""
    missing = ", ".join(missing_functions)
    return (
        f"The Moodle Feature '{feature.value}' is not available for this token/site. "
        f"Missing Moodle Web Service Function Name(s): {missing}. "
        "Run `moodle-mcp doctor` for setup guidance, or ask a Moodle admin to add "
        "the missing function(s) to the external service."
    )


async def get_available_functions(*, refresh: bool = False) -> frozenset[str] | None:
    """Return function names exposed by Site Info, or None if Moodle omits them."""
    global _available_functions_cache, _available_functions_loaded  # noqa: PLW0603

    if _available_functions_loaded and not refresh:
        return _available_functions_cache

    data = await get_moodle_api_data(APIFunction.core_webservice_get_site_info)
    data_object = data if isinstance(data, dict) else {}
    functions = _extract_functions(data_object)
    _available_functions_cache = frozenset(functions) if functions else None
    _available_functions_loaded = True
    return _available_functions_cache


def reset_available_functions_cache() -> None:
    """Clear cached function metadata."""
    global _available_functions_cache, _available_functions_loaded  # noqa: PLW0603

    _available_functions_cache = None
    _available_functions_loaded = False


def required_function_names(feature: MoodleFeature) -> list[str]:
    """Return required Moodle Web Service Function Names for a Moodle Feature."""
    return [function.value for function in FEATURE_REQUIREMENTS[feature]]


def build_capability_report(
    available_functions: Iterable[str] | None,
    *,
    include_writes: bool = True,
) -> ServerCapabilityReport:
    """Build availability from known function names."""
    available = frozenset(available_functions) if available_functions is not None else None
    features = [
        _feature_availability(feature, available)
        for feature in FEATURE_REQUIREMENTS
        if include_writes or feature not in WRITE_FEATURES
    ]
    expected = sorted(
        {function.value for functions in FEATURE_REQUIREMENTS.values() for function in functions}
    )
    return ServerCapabilityReport(
        available_functions_known=available is not None,
        expected_functions=expected,
        available_functions=sorted(available or []),
        features=features,
    )


def _feature_availability(
    feature: MoodleFeature,
    available_functions: frozenset[str] | None,
) -> FeatureAvailability:
    required = required_function_names(feature)
    if available_functions is None:
        return FeatureAvailability(
            feature=feature.value,
            status="unknown",
            required_functions=required,
            note="This Moodle site did not expose function availability in Site Info.",
        )

    missing = [function for function in required if function not in available_functions]
    if missing:
        return FeatureAvailability(
            feature=feature.value,
            status="missing_function",
            required_functions=required,
            missing_functions=missing,
        )
    return FeatureAvailability(
        feature=feature.value,
        status="available",
        required_functions=required,
    )


def _extract_functions(data: JsonObject) -> list[str]:
    functions: list[str] = []
    for item in object_list(data.get("functions")):
        name = as_optional_str(item.get("name"))
        if name is not None:
            functions.append(name)

    raw_functions = data.get("functions")
    if isinstance(raw_functions, list):
        functions.extend(item for item in raw_functions if isinstance(item, str))
    return sorted(set(functions))
