---
name: moodle-client
description: Moodle REST client behavior.
globs: ["src/moodle_mcp/moodle/**/*.py", "src/moodle_mcp/api/**/*.py"]
---
- Use async `httpx`.
- Use POST for Moodle REST calls.
- Mask tokens and private Moodle data.
- Keep retries and rate limits near the client boundary.
