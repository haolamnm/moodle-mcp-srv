"""Constrained string aliases for Pydantic validation boundaries."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, HttpUrl, SecretStr, StringConstraints
from pydantic_extra_types.color import Color
from pydantic_extra_types.country import CountryAlpha2, CountryAlpha3
from pydantic_extra_types.currency_code import ISO4217
from pydantic_extra_types.language_code import ISO639_3, LanguageAlpha2
from pydantic_extra_types.mime_types import MimeType as StrictMimeType
from pydantic_extra_types.script_code import ISO_15924
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_extra_types.timezone_name import TimeZoneName

MoodleApiUrl = HttpUrl
MoodleApiToken = SecretStr
MoodlePortalUrl = HttpUrl
MoodleColor = Color
MoodleCountryCode = CountryAlpha2
MoodleCountryAlpha3 = CountryAlpha3
MoodleCurrencyCode = ISO4217
MoodleLanguageCode = LanguageAlpha2
MoodleLanguageAlpha3 = ISO639_3
MoodleStrictMimeType = StrictMimeType
MoodleScriptCode = ISO_15924
MoodleSemanticVersion = SemanticVersion
MoodleTimeZoneName = TimeZoneName

NonEmptyText = Annotated[
    str,
    StringConstraints(min_length=1, strip_whitespace=True),
    Field(description="Non-empty text."),
]

NonEmptyHtml = Annotated[
    str,
    StringConstraints(min_length=1, strip_whitespace=True),
    Field(description="Non-empty HTML or rich text."),
]

MoodleText = Annotated[
    str,
    Field(description="Text returned by Moodle."),
]

MoodleHtml = Annotated[
    str,
    Field(description="HTML or rich text returned by Moodle."),
]

CourseShortName = Annotated[
    str,
    StringConstraints(min_length=1, max_length=100, strip_whitespace=True),
    Field(description="Moodle course shortname."),
]

MoodleUsername = Annotated[
    str,
    StringConstraints(min_length=1, max_length=100, strip_whitespace=True),
    Field(description="Moodle username."),
]

MoodleUrlString = Annotated[
    str,
    StringConstraints(pattern=r"^https?://"),
    Field(description="HTTP(S) Moodle URL serialized as a string."),
]

MoodlePluginFileUrl = Annotated[
    str,
    StringConstraints(pattern=r"^https?://"),
    Field(description="HTTP(S) Moodle pluginfile download URL."),
]

MoodleResourceUri = Annotated[
    str,
    StringConstraints(pattern=r"^moodle://[A-Za-z0-9_./{}-]+$"),
    Field(description="Read-only moodle:// resource URI."),
]

MoodleFunctionName = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_]*$"),
    Field(description="Exact Moodle Web Service Function Name."),
]

MoodleFeatureName = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_]*$"),
    Field(description="App-level Moodle Feature name."),
]

MoodleModuleName = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z0-9_]*$"),
    Field(description="Moodle activity module name."),
]

MoodleFilePath = Annotated[
    str,
    StringConstraints(min_length=1, strip_whitespace=True),
    Field(description="Moodle file path."),
]

MoodleMimeType = Annotated[
    str,
    StringConstraints(pattern=r"^[\w.+-]+/[\w.+-]+$"),
    Field(description="Moodle MIME type text."),
]

MoodleGradePercentText = Annotated[
    str,
    StringConstraints(pattern=r"^\d+(\.\d+)?\s?%$"),
    Field(description="Moodle formatted grade percentage text."),
]

MoodleIsoDateTimeText = Annotated[
    str,
    StringConstraints(min_length=1, strip_whitespace=True),
    Field(description="ISO formatted date/time text."),
]
