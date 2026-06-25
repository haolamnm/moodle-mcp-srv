---
name: models
description: Pydantic model conventions.
globs: ["src/moodle_mcp/models/**/*.py"]
---
- Keep models narrow and domain-named.
- Prefer explicit fields over loose dictionaries.
- Use aliases only at external API boundaries.
- Keep parsing logic out of unrelated modules.
