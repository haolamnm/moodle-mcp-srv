# Tools Context

Local language for FastMCP-facing tool wrappers in `moodle_mcp.tools`.

## Language

**Tool Wrapper**:
A FastMCP-exposed function that delegates to `moodle_mcp.api`.
_Avoid_: Endpoint, handler

**Tool Registry**:
The package-level registration path that adds domain tools to the shared FastMCP server.
_Avoid_: Router, controller

**Tool Domain**:
A grouping that matches a Moodle domain: courses, assignments, grades, quizzes, or forums.
_Avoid_: Feature bucket, command group
