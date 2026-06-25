# Agent Documentation Guide

Agent-facing documentation for `moodle-mcp-srv` lives here. Keep it compact, source-linked, and optimized for coding agents that need enough context to make correct changes without loading the whole internet.

## Source Order

1. Read repo instructions first: `AGENTS.local.md`, then root `AGENTS.md`.
2. Use `CONTEXT-MAP.md` to find the relevant context file.
3. Use package-local `AGENTS.md` and `CONTEXT.md` files when editing a package that has them.
4. Use `pyproject.toml`, `.python-version`, and `.env.example` for runtime and tool facts.
5. Read local source before changing behavior.
6. Use [`source-map.md`](./source-map.md) when library behavior, CLI behavior, or Moodle API details may have changed.

## External Context Map

Use [`source-map.md`](./source-map.md). Prefer `llms.txt` when the project exposes one; otherwise prefer clean Markdown, then canonical HTML.

## Documentation Shape

Use an audience-first structure:

- `docs/agents/`: routing, project invariants, source maps, and machine-friendly maintenance notes.
- `docs/human/`: human guides and narrative docs.

When adding docs, choose one type and keep it distinct:

- Tutorial: learning path for a first successful run.
- How-to: task steps for a known goal.
- Reference: factual API, config, command, or schema details.
- Explanation: design reasoning and tradeoffs.

This keeps the docs scalable without turning every page into a mixed guide.

## Writing Rules

- Keep titles literal. Prefer `Agent Documentation Guide`, `Moodle API Reference Notes`, or `Development How-To`.
- Use canonical terms from the relevant `CONTEXT.md` discovered through `CONTEXT-MAP.md`.
- Link to official docs instead of copying external documentation.
- Record source URLs directly in the page that depends on them.
- Date only volatile claims, such as current library behavior or tested external endpoints.
- Keep agent docs short enough to fit in context. Split long references into focused pages.
- Do not document speculative architecture. Document the code that exists or an accepted decision.

## Project Checks

Before docs claim a command or architecture rule, verify it locally when possible:

```sh
uv run ruff format --check
uv run ruff check
uv run ty check
uv run lint-imports
uv run bandit -c pyproject.toml -r src main.py
uv run pytest -n auto
```
