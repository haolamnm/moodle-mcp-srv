# API Context

Local language for Moodle API-facing tool implementations in `moodle_mcp.api`.

## Language

**API Function**:
An async Python function that implements tool behavior by calling Moodle, parsing the response, and returning response models.
_Avoid_: Tool, endpoint, command

**Raw Moodle Response**:
The untrusted JSON value returned by Moodle before coercion and model construction.
_Avoid_: Payload, result blob

**Coercion Helper**:
A small pure function that converts a Raw Moodle Response value into a safe primitive, object, or array.
_Avoid_: Parser, validator

**Deadline Window**:
The inclusive `now <= duedate <= cutoff` time range used for upcoming Assignment and Quiz deadlines.
_Avoid_: Lookahead range, due filter
