"""JSON types returned by Moodle."""

from __future__ import annotations

type JsonValue = str | int | float | bool | list[JsonValue] | dict[str, JsonValue] | None
type JsonObject = dict[str, JsonValue]
type JsonArray = list[JsonValue]
type MoodleResponse = JsonObject | JsonArray
