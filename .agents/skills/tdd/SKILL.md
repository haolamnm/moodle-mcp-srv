---
name: tdd
description: Build or fix behavior through one red-green-refactor slice at a time.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# TDD

Use this for behavior changes, bug fixes, FastMCP contracts, Moodle parsing, date windows, write safety, and CLI behavior.

## Principles

- Test behavior through public interfaces.
- One behavior, one failing test, one implementation step.
- Prefer vertical slices over writing all tests first.
- Never refactor while red.
- Mock Moodle HTTP; do not hit live Moodle unless explicitly opted in.

## Workflow

1. Read `CONTEXT-MAP.md` and relevant `CONTEXT.md`.
2. Name the public interface under test.
3. Write one focused failing test.
4. Run the targeted test and confirm it fails for the expected reason.
5. Implement the smallest code change.
6. Run the targeted test until green.
7. Refactor only after green.
8. Repeat for the next behavior.

## Test Surfaces

- Moodle transport: fake `httpx.AsyncClient` or `pytest-httpx`.
- Tool contracts: FastMCP in-memory client.
- Parsing helpers: direct unit tests and Hypothesis when pure.
- CLI behavior: Typer runner or subprocess only when necessary.

## Final Checks

- `uv run pytest -n auto`
- `uv run ruff check`
- `uv run ty check`
- `uv run basedpyright`
