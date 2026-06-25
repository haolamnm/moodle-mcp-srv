# Moodle Package

Moodle REST transport and Web Service primitives live here; this package knows how requests are sent but not how tool responses are shaped.

## Conventions

- Use POST form data for Moodle Web Service calls so tokens and submitted content stay out of URLs.
- Add Web Service function names to `functions.py` before using them from `moodle_mcp.api`.
- Keep request parameter formatting in small helpers such as `format_array_params`.
- Use canonical terms from `CONTEXT-MAP.md` and this package's `CONTEXT.md`.

## Gotchas

- Moodle returns application-level errors as HTTP 200 responses containing `errorcode`.
- Settings are validated when the client needs them, not at import time.
- The current user ID is cached; tests that touch it must reset the cache.
- Do not parse domain-specific Moodle response bodies in this package.

## Testing

- Test transport behavior with fake `httpx.AsyncClient` classes, not real Moodle calls.
- Cover HTTP errors, Moodle error responses, network errors, request parameters, and user ID caching.
- Verify focused changes with `uv run pytest -n auto tests/test_moodle.py`.

## Out Of Scope

- FastMCP tool registration.
- Domain response parsing.
- Pydantic response model design.
