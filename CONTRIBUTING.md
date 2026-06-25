# Contributing

Thanks for improving `moodle-mcp-srv`. Keep changes focused, typed, and safe for Moodle data.

## Setup

```sh
uv sync --all-groups
cp .env.example .env.local
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Local Checks

```sh
uv run ruff check
uv run ruff format --check
uv run ty check
uv run basedpyright
uv run lint-imports
uv run bandit -c pyproject.toml -r src main.py
uv run deptry .
uv run detect-secrets scan --baseline .secrets.baseline
uv run pip-audit
uv run pytest -n auto
```

## Rules

- Prefer intent-level MCP tools over raw Moodle Web Service wrappers.
- Return structured Pydantic models for tool responses.
- Keep resources read-only.
- Keep write tools dry-run first and require `reason` for real writes.
- Keep examples generic. Never include real Moodle URLs, tokens, course names, grades, submissions, or user data.
- Use Conventional Commits.
