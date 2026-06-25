---
name: domain-modeling
description: Maintain Moodle MCP domain language and update CONTEXT.md only when terminology is resolved.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Domain Modeling

Use this when naming, renaming, or clarifying Moodle MCP concepts. Do not use it merely to read existing context.

## Workflow

1. Read `CONTEXT-MAP.md`.
2. Read the narrowest relevant `CONTEXT.md`.
3. Challenge fuzzy or conflicting terms before writing code.
4. Resolve the canonical term with the user or from code evidence.
5. Update only the narrowest applicable `CONTEXT.md`.

## Context Rules

- `CONTEXT.md` is a glossary, not a spec.
- Keep definitions to one or two sentences.
- Include `_Avoid_:` synonyms when they help prevent drift.
- Do not add general programming terms.
- Do not include implementation decisions, file paths, or issue plans.

## Moodle MCP Examples

- Prefer **Moodle Web Service Call** over REST call when referring to the Moodle transport primitive.
- Prefer **Tool Wrapper** over endpoint or handler when referring to FastMCP-exposed functions.
- Prefer **Response Model** over DTO or schema object.

## ADR Handoff

Offer an ADR only when the decision is hard to reverse, surprising without context, and the result of a real trade-off. Use the `adr` skill for the actual file.

## Verification

- Run `rg` for existing term usage before introducing a new term.
- If docs changed only, run `git diff --check`.
- If code names changed, run targeted tests and type checks.
