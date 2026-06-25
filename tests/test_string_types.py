from __future__ import annotations

from pydantic import TypeAdapter, ValidationError
import pytest

from moodle_mcp.models import (
    CourseShortName,
    MoodleColor,
    MoodleCountryCode,
    MoodleCurrencyCode,
    MoodleFunctionName,
    MoodleLanguageCode,
    MoodleMimeType,
    MoodlePluginFileUrl,
    MoodleResourceUri,
    MoodleScriptCode,
    MoodleSemanticVersion,
    MoodleStrictMimeType,
    MoodleTimeZoneName,
    NonEmptyHtml,
)


def test_core_string_aliases_validate_expected_values() -> None:
    assert (
        TypeAdapter(MoodleFunctionName).validate_python("core_webservice_get_site_info")
        == "core_webservice_get_site_info"
    )
    assert TypeAdapter(CourseShortName).validate_python(" BIO101 ") == "BIO101"
    assert (
        TypeAdapter(MoodleResourceUri).validate_python("moodle://courses/{courseid}/overview")
        == "moodle://courses/{courseid}/overview"
    )
    assert TypeAdapter(NonEmptyHtml).validate_python(" <p>Hello</p> ") == "<p>Hello</p>"


def test_core_string_aliases_reject_invalid_values() -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(MoodleFunctionName).validate_python("Core Webservice")
    with pytest.raises(ValidationError):
        TypeAdapter(MoodleResourceUri).validate_python("https://moodle.test")
    with pytest.raises(ValidationError):
        TypeAdapter(NonEmptyHtml).validate_python("   ")


def test_url_and_mime_aliases_validate_expected_values() -> None:
    assert (
        TypeAdapter(MoodlePluginFileUrl).validate_python(
            "https://moodle.test/pluginfile.php/1/prompt.pdf"
        )
        == "https://moodle.test/pluginfile.php/1/prompt.pdf"
    )
    assert TypeAdapter(MoodleMimeType).validate_python("application/pdf") == "application/pdf"
    assert TypeAdapter(MoodleStrictMimeType).validate_python("application/pdf") == "application/pdf"


def test_extra_type_aliases_validate_expected_values() -> None:
    assert str(TypeAdapter(MoodleColor).validate_python("#336699")) == "#369"
    assert TypeAdapter(MoodleCountryCode).validate_python("VN") == "VN"
    assert TypeAdapter(MoodleCurrencyCode).validate_python("USD") == "USD"
    assert TypeAdapter(MoodleLanguageCode).validate_python("vi") == "vi"
    assert TypeAdapter(MoodleScriptCode).validate_python("Latn") == "Latn"
    assert str(TypeAdapter(MoodleSemanticVersion).validate_python("1.2.3")) == "1.2.3"
    assert TypeAdapter(MoodleTimeZoneName).validate_python("Asia/Ho_Chi_Minh") == (
        "Asia/Ho_Chi_Minh"
    )
