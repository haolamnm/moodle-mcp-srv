---
name: ship-pr
description: Ship current work through a GitHub pull request using git and gh.
metadata:
  author: haolamnm
  version: "0.1.0"
---

# Ship PR

Use when the user says `/ship-pr`, "open a PR", "ship this branch", or asks to move completed work into review.

## Preconditions

- Requires `git` and authenticated `gh` CLI.
- Never push directly to `main`.
- Never force-push unless the user explicitly asks.
- Never commit, push, or open a PR with private Moodle data, tokens, `.env`, or local MCP/client configs.

## Workflow

1. Inspect state:
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`
   - `gh auth status`
2. If on `main`, stop and create or ask for a feature branch before shipping.
3. If dirty, group changes into atomic Conventional Commit proposals. Ask before committing.
4. Fetch and compare with main:
   - `git fetch origin main`
   - `git log origin/main..HEAD --oneline`
   - `git diff origin/main...HEAD --stat`
5. Run relevant checks from `CONTRIBUTING.md`. At minimum run lint/type checks and targeted tests for touched code.
6. Read `.github/pull_request_template.md` and draft a concise PR body from real commits, diff, and checks.
7. Push the branch with `git push origin <branch>`.
8. Create the PR with `gh pr create --base main --head <branch> --title "<conventional title>" --body "<body>"`.
9. Report the PR URL, branch, commits, checks run, and any remaining risks.

## PR Body Rules

- Follow the repo PR template.
- Include concrete verification commands and outcomes.
- Mention skipped checks explicitly.
- Keep Moodle examples generic; never include live course names, grades, submissions, users, private URLs, or tokens.

## Blockers

Block shipping when checks fail, the branch contains unrelated private/local files, commits are WIP/debug-only, `gh` is unauthenticated, or the diff includes unreviewed generated churn.
