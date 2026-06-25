# Tools Package

FastMCP tool wrappers live here; they expose stable tool names and delegate behavior to `moodle_mcp.api`.

## Conventions

- Keep wrappers thin: validate the public signature, preserve the docstring, then call the matching API function.
- Register tools by domain through `registry.py`.
- Use canonical terms from `CONTEXT-MAP.md` and this package's `CONTEXT.md`.

## Gotchas

- FastMCP uses function signatures and return annotations to build tool schemas, so avoid runtime-only tricks that hide types.
- Do not put Moodle REST parsing or HTTP calls in this package.
- Preserve existing tool names unless the user explicitly accepts a breaking change.

## Testing

- Update `tests/test_tools.py` when adding, renaming, or removing a tool.
- Verify registration with `uv run pytest -n auto tests/test_tools.py`.

## Out Of Scope

- Moodle API response parsing.
- Pydantic response model design.
- Settings, logging, and transport configuration.
