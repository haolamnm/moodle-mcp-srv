---
name: codebase-design
description: Shared vocabulary for designing deep modules, interfaces, seams, and adapters.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Codebase Design

Use this when designing or refactoring `moodle-mcp-srv` modules, especially when deciding where a testable seam belongs.

## Vocabulary

- **Module**: anything with an interface and implementation. Can be a function, package, CLI command, FastMCP registry, Moodle client, or resource serializer.
- **Interface**: everything a caller must know: signature, invariants, errors, ordering, data shape, configuration, and performance expectations.
- **Implementation**: code behind the interface.
- **Seam**: a place where behavior can vary without editing callers.
- **Adapter**: a concrete implementation that sits at a seam, such as real Moodle HTTP transport or a mock Moodle server.
- **Depth**: leverage exposed through a small interface.
- **Leverage**: more behavior per concept a caller must learn.
- **Locality**: changes, bugs, and tests stay concentrated.

## Principles

- Prefer deep modules: small interface, meaningful behavior behind it.
- Use the deletion test: if deleting a module only moves pass-through code, the module is shallow.
- The interface is the test surface. Tests should cross the same seam as callers.
- One adapter means a hypothetical seam. Two adapters means a real seam.
- Do not use "service", "component", "API", or "boundary" when one of the terms above is more precise.

## Moodle MCP Fit

- Moodle Web Service Call is a transport seam.
- FastMCP Tool Wrapper signatures are agent-facing interfaces.
- Pydantic Response Models are structured output interfaces.
- `resources` serialize read-only context; they should not become write adapters.

## Verification

- For code changes, run targeted tests first.
- Before finishing implementation work, run `uv run ruff check`, `uv run ty check`, `uv run basedpyright`, and relevant pytest commands.
