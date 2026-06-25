# Models Package

Typed response models live here; they define the structured shapes returned by Moodle MCP tools.

## Conventions

- Prefer explicit Pydantic models over loose dictionaries for tool responses.
- Keep model names aligned with canonical terms from `CONTEXT-MAP.md`.
- Keep shared JSON aliases in `json.py`.
- Keep constrained string aliases in `strings.py`.
- Use `MoodleText` and `MoodleHtml` for tolerant raw Moodle text fields.
- Use `NonEmptyText` and `NonEmptyHtml` for user-supplied tool inputs that must not be blank.

## Gotchas

- FastMCP and Pydantic may need model references available at runtime, so use type-only imports only when schema generation still works.
- Avoid adding validation that changes Moodle data semantics unless an API function already normalizes that behavior.
- Do not duplicate Moodle raw response objects here; model the tool-facing response.
- Do not add email-specific aliases until the project has a real email field.

## Testing

- Run `uv run ty check` after model changes.
- Run `uv run basedpyright` after model or alias changes.
- Update `tests/test_string_types.py` when adding a String Alias.
- Run `uv run pytest -n auto` when response shapes change.

## Out Of Scope

- HTTP transport and Moodle API calls.
- FastMCP registration.
- Business logic for filtering, sorting, or aggregating Moodle data.
