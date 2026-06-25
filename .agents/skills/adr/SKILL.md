---
name: adr
description: Record durable architectural decisions in docs/adr with compact context and consequences.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# ADR

Use this when a decision should be remembered because future agents or maintainers would otherwise reopen it.

## When To Write

Write an ADR only when all are true:

- The decision is hard to reverse.
- The choice is surprising without context.
- There were real alternatives and a trade-off.

Skip ADRs for obvious choices, temporary plans, routine library usage, or decisions already captured in code and context.

## Location

- ADRs live in `docs/adr/`.
- Use sequential filenames: `0001-short-slug.md`, `0002-short-slug.md`.
- Scan existing ADRs before choosing a number.

## Format

```md
# Short Decision Title

Status: accepted

Context: one or two short paragraphs.

Decision: what we chose.

Consequences: what this makes easier and harder.
```

Keep it compact. Optional sections are fine only when they add signal.

## Moodle MCP ADR Candidates

- Public MCP contract stability policy.
- Moodle Web Service compatibility strategy.
- Write safety model.
- Packaging and release channel choices.
- Architectural seams around Moodle transport, feature detection, caching, or resources.

## Verification

- Check for existing ADR conflicts.
- Link to source docs or code paths when useful.
- Run `git diff --check`.
