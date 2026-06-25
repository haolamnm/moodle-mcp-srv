---
name: diagnosing-bugs
description: Diagnose hard bugs by building a tight repro loop before changing code.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Diagnosing Bugs

Use this when something is broken, flaky, slow, or surprising. Do not start with a theory. Start with a feedback loop.

## Phase 1: Build A Red-Capable Loop

Create one command that can catch the exact symptom.

Good loops for this repo:

- A focused pytest reproducing Moodle response parsing.
- A `pytest-httpx` test for a Moodle Web Service Call.
- A FastMCP in-memory client test for tool/resource behavior.
- A CLI test for `moodle-mcp doctor`, `ping`, `inspect`, or `serve`.
- A mocked Moodle smoke test profile.

Live Moodle tests require explicit opt-in and must avoid private output.

## Phase 2: Reproduce And Minimize

- Confirm the loop fails for the user's actual symptom.
- Cut inputs and setup until every remaining piece is load-bearing.
- Keep the minimized repro as the regression test when possible.

## Phase 3: Hypothesize

List 3 to 5 ranked, falsifiable hypotheses. Each hypothesis must predict what would change if it is true.

## Phase 4: Probe

- Change one variable at a time.
- Use targeted logs only when needed.
- Prefix temporary logs with a unique marker and remove them before finishing.

## Phase 5: Fix And Verify

- Write or keep the regression test.
- Apply the smallest fix.
- Re-run the minimized repro and original loop.
- Run relevant static checks.

## Finish Criteria

- Original symptom no longer reproduces.
- Regression test exists or lack of a good seam is documented.
- Temporary debugging code is gone.
- Final answer names the cause and verification.
