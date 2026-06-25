# Typed Python

Use this note before changing Pydantic models, FastMCP tool parameters, or Moodle string aliases.

## Rules

- Put meaningful string aliases in `src/moodle_mcp/models/strings.py`.
- Use Pydantic aliases at validation boundaries; use plain `str` only when the value has no domain meaning.
- Use `SecretStr` for Moodle tokens and unwrap only when calling Moodle.
- Use `StrEnum` for finite protocol values such as Moodle Web Service Function names.
- Keep raw Moodle response text tolerant with `MoodleText` or `MoodleHtml`.
- Use `NonEmptyText` or `NonEmptyHtml` for required user-supplied tool input.
- Do not add `EmailStr`, `pydantic[email]`, or direct email aliases until the codebase has a real email field.
- Test new aliases in `tests/test_string_types.py`.
- Run `uv run ty check`, `uv run basedpyright`, `uv run ruff check`, and `uv run pytest -n auto`.

## External Docs

- Pydantic: `https://pydantic.dev/llms.txt`
- Pydantic Extra Types: `https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/`
