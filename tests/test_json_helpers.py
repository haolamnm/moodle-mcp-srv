from __future__ import annotations

import pytest

from moodle_mcp.api import coercion


def test_json_helpers_coerce_expected_values() -> None:
    assert coercion.as_object({"name": "Course"}) == {"name": "Course"}
    assert coercion.as_object("not-object") == {}
    assert coercion.object_list([{"id": 1}, "skip", {"id": 2}]) == [{"id": 1}, {"id": 2}]
    assert coercion.as_array([1, "two"]) == [1, "two"]
    assert coercion.as_array("not-array") == []
    assert coercion.as_str("value") == "value"
    assert coercion.as_str(None, "fallback") == "fallback"
    assert coercion.as_optional_str("value") == "value"
    assert coercion.as_optional_str(1) is None
    assert coercion.as_int("42") == 42
    assert coercion.as_int("bad", 7) == 7
    assert coercion.as_optional_int(True) is None
    assert coercion.as_optional_int(4.5) == 4
    assert coercion.as_optional_float("4.5") == pytest.approx(4.5)
    assert coercion.as_optional_float(False) is None
    assert coercion.as_optional_float("bad") is None
    assert coercion.as_bool(True) is True
    assert coercion.as_bool(0) is False
    assert coercion.as_bool("yes") is True
    assert coercion.as_bool(None, True) is True
