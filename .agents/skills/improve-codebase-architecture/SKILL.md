---
name: improve-codebase-architecture
description: Audit architectural friction and propose concrete deepening candidates without editing first.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Improve Codebase Architecture

Use this for architecture audits, modularity questions, and testability problems. This skill uses `codebase-design` vocabulary.

## Workflow

1. Read `CONTEXT-MAP.md` and relevant `CONTEXT.md`.
2. Read existing ADRs in `docs/adr/` if present.
3. Inspect code paths organically; do not rely only on file names.
4. Look for shallow modules, leaky seams, scattered logic, and tests that must reach past public interfaces.
5. Present 3 or fewer refactor candidates.
6. Do not edit code until the user picks a candidate.

## Candidate Shape

For each candidate, include:

- Files or packages involved.
- Current friction.
- Proposed seam or deeper module.
- Why this improves leverage, locality, or testability.
- Risk and migration shape.
- Recommendation strength: `strong`, `worth exploring`, or `speculative`.

## Moodle MCP Review Targets

- `moodle_mcp.moodle`: transport, retries, rate limits, feature detection, and cache seams.
- `moodle_mcp.api`: parsing and domain behavior.
- `moodle_mcp.tools`: thin FastMCP wrappers and stable tool signatures.
- `moodle_mcp.resources`: read-only context serialization.
- `moodle_mcp.models`: response model boundaries.
- `moodle_mcp.cli`: Typer command composition.

## ADR Handoff

If a candidate is rejected for a durable reason, offer an ADR. Do not create one unless the user agrees.

## Verification

Architecture reports do not require tests. If code changes follow, use `implement` and relevant checks.
