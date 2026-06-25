# moodle-mcp-srv

Your Moodle dashboard, available to AI.

FastMCP server exposing Moodle courses, assignments, grades, quizzes, forums, announcements, and calendar events as MCP tools, resources, and prompts.

`moodle-mcp-srv` is an independent project. It is not affiliated with, endorsed by, or sponsored by Moodle Pty Ltd.

## Status

- Project status: pre-1.0 public preview.
- Python: 3.13+.
- Moodle compatibility: best effort; site support depends on enabled Moodle Web Service functions.
- API stability: MCP tool names and response schemas may change before 1.0.
- Support: GitHub issues for bugs and feature requests; private security reports for vulnerabilities.

## Safety Model

- Moodle remains the source of truth for authorization.
- Moodle Feature availability checks are setup guidance, not an authorization system.
- Use a least-privilege Moodle web-service token.
- The server does not need your Moodle username or password.
- MCP clients can see Moodle data returned by tools and resources.
- Write tools default to `dry_run=True`; real writes require explicit user confirmation and `reason`.
- Do not expose HTTP transport publicly without authentication and reverse-proxy controls.
- Do not commit live Moodle logs, fixtures, course names, grades, submissions, or user data.

## Non-Goals

- This is not an official Moodle product.
- This is not a Moodle plugin.
- This does not bypass Moodle permissions.
- This does not store Moodle credentials.
- This does not provide a hosted SaaS.
- This does not guarantee compatibility with every Moodle plugin or custom Web Service function.

## Installation

```sh
uv sync
cp .env.example .env
```

Set these as OS environment variables, or put them in `.env` / `.env.local`:

```sh
MOODLE_API_URL=https://moodle.example.edu/webservice/rest/server.php
MOODLE_API_TOKEN=your_token
```

Precedence is OS environment variables, then `.env.local`, then `.env`.

Replace `moodle.example.edu` with your Moodle portal host. If your portal is `https://moodle.example.edu`, the API URL is usually:

```sh
MOODLE_API_URL=https://moodle.example.edu/webservice/rest/server.php
```

To find a token, log in to Moodle and check:

```text
https://moodle.example.edu/user/managetoken.php
```

Some Moodle sites hide or disable self-service tokens. In that case, ask the Moodle admin for a web-service token for your account.

Quick connection check after setting credentials:

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

Published package usage:

```sh
uvx --from moodle-mcp-srv moodle-mcp
```

See `examples/` for MCP client snippets for VS Code, Zed, Claude Desktop, Claude Code, Codex, Gemini CLI, OpenCode, Factory Droid, and Pi Code.

## Tool Surface

The server exposes intent-level tools and read-only `moodle://` resources for Moodle context. Run:

```sh
uv run moodle-mcp inspect
uv run moodle-mcp doctor
```

`doctor` checks configuration, the Moodle connection, Site Info, expected Web Service functions, and feature availability.

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

## Release Notes

See `CHANGELOG.md`.

## Security

See `SECURITY.md`.

## License

Apache-2.0. See `LICENSE`.

## For Agents

- Start with `get_site_info` for Moodle site/version metadata, then `get_my_courses` to discover enrolled courses.
- Prefer `moodle://` resources for read-only context when available.
- Write tools default to `dry_run=True`; pass `dry_run=False` only after explicit user confirmation and include `reason`.
- Tools are cross-course by default when they accept `course_ids`.
- Use `course_ids` to narrow assignment, grade, quiz, and announcement queries.
- Use `CONTEXT-MAP.md` to find canonical terms before changing tool names or response shapes.
- Timestamps from Moodle are Unix timestamps unless an `_iso` field is present.
