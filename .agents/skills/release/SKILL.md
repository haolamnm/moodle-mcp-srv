---
name: release
description: Cut a GitHub release by updating changelog, validating release checks, creating a tag, and publishing with gh.
metadata:
  author: haolamnm
  version: "0.1.0"
---

# Release

Use when the user says `/release`, "cut a release", "tag a version", or asks to publish a new version.

## Preconditions

- Requires `git` and authenticated `gh` CLI.
- Release from `main` only.
- Do not create tags or GitHub releases without explicit user confirmation.
- Read `docs/release-checklist.md`, `CHANGELOG.md`, and `pyproject.toml` before changing anything.

## Workflow

1. Inspect state:
   - `git status --short`
   - `git branch --show-current`
   - `git fetch origin main --tags`
   - `git log origin/main..HEAD --oneline`
   - `gh auth status`
2. Block if not on `main`, dirty without confirmed release edits, behind `origin/main`, or missing `gh` auth.
3. Determine the target version from the requested bump, `pyproject.toml`, existing tags, and unreleased commits.
4. Update `CHANGELOG.md` with concise user-facing entries grouped as major, minor, or patch. Include commit hashes when available.
5. If the version changes, update project version metadata using the repo's configured tooling or the smallest direct edit.
6. Run the release checklist checks that fit the changed surface. Do not skip failed checks silently.
7. Commit release prep with `chore(release): vX.Y.Z` after confirmation.
8. Create an annotated tag: `git tag -a vX.Y.Z -m "vX.Y.Z"`.
9. Push the commit and tag only after confirmation:
   - `git push origin main`
   - `git push origin vX.Y.Z`
10. Create the GitHub release with `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notes>`.

## Changelog Rules

- Keep `CHANGELOG.md` compact and reverse chronological.
- Describe user-visible changes, not implementation trivia.
- Separate breaking changes from features, fixes, docs, and maintenance.
- Keep Moodle examples generic; never include live course names, grades, submissions, users, private URLs, or tokens.

## Blockers

Block release when checks fail, version/tag already exists, release notes are unclear, private Moodle data appears in docs/examples, PyPI release settings are not confirmed, or repository settings still need human action.
