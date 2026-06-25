# Moodle Context

Local language for Moodle REST transport primitives in `moodle_mcp.moodle`.

## Language

**Moodle Web Service Call**:
A POST form request to Moodle's REST endpoint with `wstoken`, `wsfunction`, `moodlewsrestformat`, and function parameters.
_Avoid_: REST call, endpoint call

**Web Service Function Name**:
The exact Moodle function string represented by `APIFunction`.
_Avoid_: Method name, operation

**Moodle API Error**:
The project exception raised for Moodle HTTP, network, or application-level errors.
_Avoid_: Client error, transport error

**Array Parameter**:
A Moodle-style indexed parameter such as `courseids[0]`.
_Avoid_: List parameter, repeated parameter
