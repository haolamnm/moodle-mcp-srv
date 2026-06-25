---
name: tests
description: Test strategy and coverage.
globs: ["tests/**/*.py"]
---
- Mirror `src/` structure where practical.
- Reproduce bugs before fixing them.
- Prefer mocked Moodle HTTP over live Moodle.
- Use FastMCP in-memory tests for MCP behavior.
