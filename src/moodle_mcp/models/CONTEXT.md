# Models Context

Local language for typed tool response shapes in `moodle_mcp.models`.

## Language

**Response Model**:
A typed Pydantic model returned by one or more MCP tools.
_Avoid_: DTO, schema object

**JSON Alias**:
A recursive type alias for raw JSON-like Moodle data before it is converted into a Response Model.
_Avoid_: Blob, any dict

**Tool-Facing Field**:
A normalized field exposed to agents, such as `due_date_iso` alongside a Moodle Unix timestamp.
_Avoid_: Convenience property, display field
