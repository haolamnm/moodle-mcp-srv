# AGENTS.md

<critical>
If `AGENTS.local.md` exists at the repo root, read it first. It contains personal tool preferences (e.g. which MCP servers to use for web and code search) that override the defaults in this file.
</critical>

We're building **moodle-mcp-srv** — an MCP (Model Context Protocol) server that bridges AI assistants with the **Moodle LMS REST API** using **FastMCP**. It exposes courses, assignments, grades, quizzes, forums, and calendar events as AI-callable tools so students can interact with their LMS through natural language.

## Domain Language

Every concept has one name. Synonyms are banned. See [`CONTEXT-MAP.md`](./CONTEXT-MAP.md) to find the relevant context file. If a term is missing, define it in the narrowest applicable `CONTEXT.md`.

## Typed Boundaries

Use typed Python to make Moodle concepts explicit, especially at Pydantic and FastMCP boundaries.

- Use `StrEnum` for finite Moodle protocol values.
- Use Pydantic constrained aliases from `moodle_mcp.models.strings` for meaningful strings.
- Use `SecretStr` for tokens and unwrap only at the transport boundary.
- Do not add `EmailStr` or `pydantic[email]` unless the project gains a real email field.
- Keep raw Moodle response fields tolerant; validate user-supplied tool inputs more strictly.

## Code Principles

### 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked. No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

### 5. Domain Integrity

Every concept has one name. Check `CONTEXT-MAP.md` before naming anything new, then read the relevant `CONTEXT.md`. If a term is missing, define it with its canonical meaning in the narrowest applicable `CONTEXT.md`.

## Project Config

Read these files to understand the project setup instead of relying on hardcoded conventions here:

- `pyproject.toml` — dependencies, tool config (ruff, pytest), build settings
- `.python-version` — Python runtime version
- `.env.example` — required environment variables

## Testing

**Framework:** `pytest` + `pytest-cov`; use `pytest-xdist` for local parallel runs and Hypothesis for property-based tests of pure helpers.

Tests live in `tests/` mirroring `src/` structure. Coverage config and thresholds are in `pyproject.toml`. Write tests for every new function or bug fix — aim to reproduce before fixing. Do not use Hypothesis for tests that hit real Moodle, wall-clock behavior, or FastMCP runtime registration.
