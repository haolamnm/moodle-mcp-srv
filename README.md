# moodle-mcp-srv

Your Moodle dashboard, available to AI.

FastMCP server exposing Moodle courses, assignments, grades, quizzes, forums, announcements, and calendar events as MCP tools, resources, and prompts.

## Installation

```sh
uv sync
cp .env.example .env
```

Set these in `.env` or `.env.local`:

```sh
MOODLE_API_URL=https://moodle.example.edu/webservice/rest/server.php
MOODLE_API_TOKEN=your_token
```

Replace `moodle.example.edu` with your Moodle portal host. If your portal is `https://moodle.example.edu`, the API URL is usually:

```sh
MOODLE_API_URL=https://moodle.example.edu/webservice/rest/server.php
```

To find a token, log in to Moodle and check:

```text
https://moodle.example.edu/user/managetoken.php
```

Some Moodle sites hide or disable self-service tokens. In that case, ask the Moodle admin for a web-service token for your account.

Quick connection check after setting `.env.local`:

```sh
uv run moodle-mcp ping
```

Setup diagnostics:

```sh
uv run moodle-mcp doctor
uv run moodle-mcp doctor --json
```

Run over stdio:

```sh
uv run moodle-mcp
```

Run over HTTP:

```sh
uv run moodle-mcp serve --http --host 127.0.0.1 --port 8000
```

Inspect the local MCP surface:

```sh
uv run moodle-mcp inspect
```

## Development

```sh
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
uv run ruff format
uv run ruff check
uv run ty check
uv run basedpyright
uv run lint-imports
uv run bandit -c pyproject.toml -r src main.py
uv run deptry .
uv run pip-audit
uv run detect-secrets scan --baseline .secrets.baseline
uv run pytest
MOODLE_MCP_RUN_LIVE_TESTS=1 uv run pytest tests/test_live_moodle_tools.py -q
uv run pytest -n auto  # optional parallel run
```

Optional MCP security scan:

```sh
uvx mcp-scan@latest inspect
```

Project layout:

```text
src/moodle_mcp/server.py    FastMCP composition root
src/moodle_mcp/tools/       Tool registration by domain
src/moodle_mcp/resources/   Read-only moodle:// context
src/moodle_mcp/prompts/     Reusable Moodle workflows
src/moodle_mcp/api/         Moodle tool implementations by domain
src/moodle_mcp/moodle/      Moodle REST client
src/moodle_mcp/models/      Typed tool response shapes
src/moodle_mcp/config/      Settings and logging
docs/agents/                Agent-facing documentation
docs/human/                 Human-facing documentation
```

## For Agents

- Start with `get_site_info` for Moodle site/version metadata, then `get_my_courses` to discover enrolled courses.
- Prefer `moodle://` resources for read-only context when available.
- Write tools default to `dry_run=True`; pass `dry_run=False` only after explicit user confirmation and include `reason`.
- Tools are cross-course by default when they accept `course_ids`.
- Use `course_ids` to narrow assignment, grade, quiz, and announcement queries.
- Use `CONTEXT-MAP.md` to find canonical terms before changing tool names or response shapes.
- Timestamps from Moodle are Unix timestamps unless an `_iso` field is present.
