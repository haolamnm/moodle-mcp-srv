# moodle-mcp-srv

All notable changes to this project are documented here.

## 0.2.0

### Minor Changes

- `a11486d` Thanks @haolamnm! — Classify tool failures as setup gaps (missing Web Service function) versus Moodle-enforced Access Errors, with distinct guidance per kind.
- `a11486d` Thanks @haolamnm! — Add the `create_calendar_event` write tool (dry-run by default, reason required when writing).
- `a11486d` Thanks @haolamnm! — Add the `mark_activity_complete` write tool for manual activity completion (dry-run by default, reason required when writing).
- `a11486d` Thanks @haolamnm! — `submit_assignment` now finalizes submissions by saving online text and then calling `mod_assign_submit_for_grading`.
- `a11486d` Thanks @haolamnm! — Add read-only resources `moodle://quizzes/{courseid}/brief`, `moodle://forums/{courseid}/digest`, and `moodle://deadlines/upcoming`.
- `a11486d` Thanks @haolamnm! — `dashboard_summary` degrades per section and reports `warnings` instead of failing the whole summary when a Web Service function is unavailable or refused.
- `a11486d` Thanks @haolamnm! — `get_upcoming_deadlines` degrades assignment and quiz sources independently.

### Patch Changes

- `a11486d` Thanks @haolamnm! — `submit_assignment` with `draft=True` no longer sends a non-standard `save` parameter.
- `a11486d` Thanks @haolamnm! — Share the `require_write_reason` write guard across API modules instead of duplicating it per module.

## 0.1.0

### Minor Changes

- `0f02889` Thanks @haolamnm! — Initial public-preview package (2026-06-25).
