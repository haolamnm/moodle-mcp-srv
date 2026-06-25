---
name: triage
description: Turn issue-like requests into clear states, missing-info questions, or agent-ready briefs.
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Triage

Use this when reviewing a bug report, feature request, PR idea, or backlog item. Default to read-only analysis unless the user explicitly asks to write to GitHub or another tracker.

## States

- `needs-triage`: maintainer evaluation is still needed.
- `needs-info`: reporter must answer specific questions.
- `ready-for-agent`: enough context exists for an agent to implement.
- `ready-for-human`: needs human judgment, credentials, manual review, or product decision.
- `wontfix`: will not be actioned.

Categories:

- `bug`
- `enhancement`

## Workflow

1. Read the request and any linked context.
2. Read `CONTEXT-MAP.md` and relevant `CONTEXT.md`.
3. Check whether the behavior already exists.
4. For bugs, verify or propose the smallest reproduction path.
5. For enhancements, identify the user-visible outcome and non-goals.
6. Recommend one category and one state with reasons.
7. If `ready-for-agent`, write a concise agent brief.

## Agent Brief Shape

```md
## Goal

## Context

## Acceptance Criteria

## Constraints

## Verification
```

## Write Safety

- Do not post comments, create labels, close issues, or modify tracker state without explicit confirmation.
- Any AI-generated tracker comment must say it was generated during triage.
- Never include private Moodle data, tokens, course names from live output, grades, submissions, or user data.
