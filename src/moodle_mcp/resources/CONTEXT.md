# Resources Context

**Resource**: a read-only MCP context endpoint addressed by a `moodle://` URI.

**Resource Template**: a parameterized Resource URI such as `moodle://courses/{courseid}/content`.

**Resource Payload**: compact text returned to the agent, usually JSON serialized from Pydantic models.

**Quiz Brief**: a Resource listing the Quizzes in one Course (`moodle://quizzes/{courseid}/brief`).

**Forum Digest**: a Resource listing the Forum Discussions in one Course (`moodle://forums/{courseid}/digest`).

**Upcoming Deadlines Resource**: a cross-course Resource of merged upcoming Deadlines (`moodle://deadlines/upcoming`).
