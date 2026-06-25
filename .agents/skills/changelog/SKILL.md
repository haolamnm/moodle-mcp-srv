---
name: changelog
description: Maintain CHANGELOG.md as meaningful merges land. Use after merging a feature branch, before cutting a release, or when asked "what changed?".
argument-hint: "[version bump: major|minor|patch]"
metadata:
  author: mattpocock
  version: "1.0.2"
---

# Changelog

Maintain `CHANGELOG.md` in the Matt Pocock format. Every meaningful merge or feature must be recorded.

## When to Use

- After merging a feature branch into main
- After a breaking change
- Before cutting a release
- When someone asks "what changed?"

## Format

```
# moodle-mcp-srv

## {version}

### Major Changes

- `{commit-short-hash}` Thanks @{author}! — {what changed, one sentence}.
- ...

### Minor Changes

- `{commit-short-hash}` Thanks @{author}! — {what changed, one sentence}.
- ...

### Patch Changes

- `{commit-short-hash}` Thanks @{author}! — {what changed, one sentence}.
- ...
```

## Rules

- **Major Changes**: breaking API, renamed packages, changed domain terms in CONTEXT.md, removed a pipeline
- **Minor Changes**: new feature, new pipeline, new retrieval path, new reranker
- **Patch Changes**: bug fixes, performance improvements, docs updates, refactors with no behavior change
- **Every entry must have a commit hash**. Get it from `git log --oneline -1` or the merge commit.
- **One sentence per entry**. Describe what changed, not how.
- **Entries are reverse chronological** within each section (newest first).
- **Don't repeat the changelog format explanation** in the file. This skill is the reference.

## Workflow

1. Run `git log --oneline -5` to find the relevant commit hashes.
2. Read `CHANGELOG.md` to see the current latest version.
3. Determine if the change is Major, Minor, or Patch.
4. If the version header for this release doesn't exist yet, create it with the appropriate bump.
5. Add the entry under the correct section.
6. Update with `edit_file` — never rewrite the whole file.
