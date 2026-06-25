---
name: typed-python
description: Strict typing expectations.
globs: ["src/**/*.py", "tests/**/*.py", "scripts/**/*.py", "pyproject.toml"]
---
- Keep public functions fully annotated.
- Avoid `Any` except at third-party boundaries.
- Use Pydantic models for structured external data.
- Keep `ty` and `basedpyright` clean.
