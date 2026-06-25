# API Package

Moodle tool implementations live here; they fetch Moodle data, normalize raw responses, and return typed response models.

## Conventions

- Keep one module per Moodle domain: courses, assignments, grades, quizzes, forums, calendar, or dashboard.
- Use `moodle_mcp.moodle` for Moodle Web Service calls and `moodle_mcp.models` for returned shapes.
- Keep response parsing close to the API function that needs it unless the helper is reused across domains.
- Use canonical terms from `CONTEXT-MAP.md` and this package's `CONTEXT.md`.

## Gotchas

- Moodle responses are inconsistent: numbers may arrive as strings, optional objects may be absent, and arrays may contain non-object values.
- Do not expose raw Moodle response objects from public API functions.
- Do not register FastMCP tools here; `moodle_mcp.tools` owns tool registration.
- Preserve time-window semantics when filtering deadlines and Calendar Events.

## Testing

- Add behavior tests under `tests/` for parsing, filtering, write-tool parameters, and error paths.
- Use Hypothesis for pure coercion or filtering helpers when the property is clearer than enumerating examples.
- Verify focused changes with `uv run pytest -n auto tests/<target>.py`.

## Out Of Scope

- HTTP transport details.
- FastMCP schemas and registration.
- Pydantic model declarations.
