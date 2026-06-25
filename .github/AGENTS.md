# AGENTS.md

This folder owns GitHub-facing project metadata: workflows, issue forms, and pull request guidance.

## Conventions

- Keep workflows based on `uv`, `.python-version`, and commands from `pyproject.toml`.
- Use least-privilege workflow permissions.
- Keep pull request and issue templates compact.
- Keep examples generic; do not include Moodle site names, tokens, or private course data.

## Gotchas

- PR workflows must not require repository secrets.
- Commit convention enforcement uses Commitizen.
- Full quality gates should stay consistent with local developer commands.

## Testing

- Validate workflow command names locally when possible.
- Run `git diff --check` after editing YAML and Markdown.

## Out Of Scope

- Release automation and package publishing.
- Live Moodle credentials or environment-specific CI secrets.
