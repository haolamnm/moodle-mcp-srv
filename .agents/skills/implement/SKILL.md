---
name: implement
description: Execute a scoped implementation plan with tests, typed Python checks, and no automatic commits.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Implement

Use this when the user has chosen a scoped change and wants it built.

## Preconditions

- Read `AGENTS.local.md`, `AGENTS.md`, `CONTEXT-MAP.md`, and relevant local `CONTEXT.md`.
- State assumptions for non-trivial work.
- Identify the smallest behavior-oriented success criteria.

## Workflow

1. Inspect current code before editing.
2. Choose existing patterns over new abstractions.
3. Prefer `tdd` for behavior changes and bug fixes.
4. Keep edits narrow.
5. Update docs/context only when contracts or domain language change.
6. Run targeted checks as you work.
7. Run the final relevant quality gate.

## Moodle MCP Guardrails

- Do not expose raw Moodle RPC wrappers as new public tools unless explicitly requested.
- Return structured Pydantic models for tool-facing data.
- Keep write operations dry-run first and `reason` protected.
- Never print tokens or private Moodle data.
- Do not hit live Moodle unless the user asks or existing live-test flags are enabled.

## Commit Policy

Do not commit unless the user explicitly asks. If asked to commit, use small Conventional Commits.

## Final Checks

Use the smallest sufficient set, then broaden when touched code is shared:

- `uv run pytest -n auto`
- `uv run ruff check`
- `uv run ruff format --check`
- `uv run ty check`
- `uv run basedpyright`
- `uv run lint-imports`
