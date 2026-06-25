---
name: mcp-contracts
description: FastMCP contract guidance.
globs: ["src/moodle_mcp/tools/**/*.py", "src/moodle_mcp/resources/**/*.py", "src/moodle_mcp/prompts/**/*.py", "src/moodle_mcp/server/**/*.py"]
---
- Expose intent-level contracts, not raw Moodle RPC names.
- Return structured models where practical.
- Write descriptions for agent routing.
- Separate read-only context from write actions.
