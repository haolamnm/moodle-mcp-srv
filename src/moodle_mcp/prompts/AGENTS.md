# Prompts

Reusable FastMCP prompts package safe Moodle workflows for agents without fetching data or writing to Moodle directly.

## Conventions

- Keep prompts short, explicit, and workflow-oriented.
- State read-only or write constraints directly in prompt text.
- Reference canonical tool/resource names when useful.

## Gotchas

- Prompts are not docs; they steer an agent through a workflow.
- Do not include secrets, private course data, or Moodle API internals.

## Testing

- Cover prompt registration and names with in-memory FastMCP client tests.
- Snapshot prompt names when they are part of the agent-facing contract.

## Out Of Scope

- Moodle fetching, parsing, and write execution.
