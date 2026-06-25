# Models Package

Typed response models live here; they define the structured shapes returned by Moodle MCP tools.

## Conventions

- Prefer explicit Pydantic models over loose dictionaries for tool responses.
- Keep model names aligned with canonical terms from `CONTEXT-MAP.md`.
- Keep shared JSON aliases in `json.py`.

## Gotchas

- FastMCP and Pydantic may need model references available at runtime, so use type-only imports only when schema generation still works.
- Avoid adding validation that changes Moodle data semantics unless an API function already normalizes that behavior.
- Do not duplicate Moodle raw response objects here; model the tool-facing response.

## Testing

- Run `uv run ty check` after model changes.
- Run `uv run pytest -n auto` when response shapes change.

## Out Of Scope

- HTTP transport and Moodle API calls.
- FastMCP registration.
- Business logic for filtering, sorting, or aggregating Moodle data.
