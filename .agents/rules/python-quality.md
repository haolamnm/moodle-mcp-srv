---
name: python-quality
description: Python style, imports, and tooling.
globs: ["src/**/*.py", "tests/**/*.py", "scripts/**/*.py", "pyproject.toml"]
---
- Use Python 3.13 syntax.
- Use `uv` for commands.
- Keep imports sorted by Ruff.
- Prefer simple functions over speculative abstractions.
