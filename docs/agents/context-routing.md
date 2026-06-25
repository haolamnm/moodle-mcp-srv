# Context Routing

Read the narrowest context that explains the code you are changing.

## Order

1. Root `AGENTS.local.md` for machine-local tool preferences.
2. Root `AGENTS.md` for project-wide rules.
3. `CONTEXT-MAP.md` to find the relevant context files.
4. Package-local `AGENTS.md` and `CONTEXT.md` when present.
5. Source files and tests for implementation truth.

## Current Package Context

| Package | Local files |
|---|---|
| `src/moodle_mcp/` | `CONTEXT.md` |
| `src/moodle_mcp/tools/` | `AGENTS.md`, `CONTEXT.md` |
| `src/moodle_mcp/api/` | `AGENTS.md`, `CONTEXT.md` |
| `src/moodle_mcp/moodle/` | `AGENTS.md`, `CONTEXT.md` |
| `src/moodle_mcp/models/` | `AGENTS.md`, `CONTEXT.md` |

## Rule

Add package-local context only when it prevents repeated mistakes or clarifies a real ownership boundary.
