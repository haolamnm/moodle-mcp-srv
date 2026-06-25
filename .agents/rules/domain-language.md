---
name: domain-language
description: Canonical naming and context rules.
globs: ["CONTEXT-MAP.md", "**/CONTEXT.md", "src/**/*.py", "tests/**/*.py", "docs/**/*.md"]
---
- Check `CONTEXT-MAP.md` before naming concepts.
- Use one canonical term per domain concept.
- Add missing terms to the narrowest `CONTEXT.md`.
- Do not invent synonyms in code, tests, or docs.
