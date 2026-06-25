# Context Map

## Contexts

- [Moodle MCP Domain](./src/moodle_mcp/CONTEXT.md) — canonical Moodle-facing language shared across the server.
- [Tools](./src/moodle_mcp/tools/CONTEXT.md) — FastMCP tool wrapper language and ownership boundaries.
- [Resources](./src/moodle_mcp/resources/CONTEXT.md) — read-only `moodle://` context URI language and ownership boundaries.
- [Prompts](./src/moodle_mcp/prompts/CONTEXT.md) — reusable Moodle workflow prompt language and safety constraints.
- [API](./src/moodle_mcp/api/CONTEXT.md) — Moodle response parsing, filtering, and tool behavior language.
- [Moodle](./src/moodle_mcp/moodle/CONTEXT.md) — Moodle REST transport and Web Service request language.
- [Models](./src/moodle_mcp/models/CONTEXT.md) — typed response model language and schema boundaries.

## Relationships

- **Moodle MCP Domain → Tools**: Tool names, signatures, and docstrings use the global Course, Assignment, Grade, Quiz, Forum, Announcement, Calendar Event, and Dashboard Summary terms.
- **Moodle MCP Domain → Resources**: Resource URIs and payloads use the global Course, Assignment, and Dashboard Summary terms.
- **Moodle MCP Domain → Prompts**: Prompts use global Moodle-facing terms and describe safe workflow sequencing.
- **Moodle MCP Domain → API**: API functions parse Moodle responses into the global Course, Assignment, Grade, Quiz, Forum, Announcement, Calendar Event, and Dashboard Summary terms.
- **Moodle MCP Domain → Models**: Response models encode the global domain terms as typed, tool-facing shapes.
- **Tools → Models**: Tools expose API results whose structured return values are declared in Models.
- **Tools → API**: Tools delegate behavior to `moodle_mcp.api`; they do not parse Moodle responses directly.
- **Resources → API**: Resources delegate Moodle reads to `moodle_mcp.api` and serialize typed results.
- **Prompts → Tools/Resources**: Prompts reference intended tool/resource sequencing but do not import or call them.
- **API → Moodle**: API functions call Moodle Web Service functions through `moodle_mcp.moodle`; they do not construct HTTP clients directly.
- **API → Models**: API functions construct Models from Moodle responses; Models stay free of fetching and filtering logic.
- **Moodle → Config**: Moodle transport reads settings through `moodle_mcp.config`; it does not depend on Tools or API.
