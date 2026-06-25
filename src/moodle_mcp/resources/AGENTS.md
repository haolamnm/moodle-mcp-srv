# Resources

Read-only FastMCP resources expose Moodle context through `moodle://` URIs for agents that need passive context instead of active tool calls.

## Conventions

- Keep resources read-only and side-effect free.
- Return compact JSON or plain text suitable for MCP context.
- Use `moodle_mcp.api` for Moodle data; do not call transport directly.

## Gotchas

- Templated resources appear through resource templates, not `list_resources()`.
- Do not expose tokens, private raw Moodle errors, or unbounded payloads.

## Testing

- Cover resource registration with in-memory FastMCP client tests.
- Mock API functions when testing resource serialization.

## Out Of Scope

- Write actions, confirmations, and permission decisions.
