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

**String Alias**:
A constrained string type used at Pydantic validation boundaries when a plain string would lose domain meaning.
_Avoid_: Branded string, custom scalar

**Tolerant Moodle Text**:
Raw text or HTML accepted from Moodle without stricter semantic validation.
_Avoid_: Display text, safe HTML

**Non-Empty Tool Input**:
User-supplied text that must contain content before a write or preview tool can proceed.
_Avoid_: Required string, mandatory text
