# Release Checklist

Use this before tagging a public release.

## Repository Settings

- Enable GitHub private vulnerability reporting.
- Protect release tags matching `v*`.
- Require the `pypi` GitHub environment for PyPI publishing.
- Keep branch protection enabled for `main`.

## Local Verification

```sh
uv run ruff check
uv run ruff format --check
uv run ty check
uv run basedpyright
uv run lint-imports
uv run bandit -c pyproject.toml -r src main.py
uv run deptry .
uv run pip-audit
uv run pre-commit run gitleaks --all-files
uv run pytest -n auto
uv build
```

## Release Verification

- Confirm `CHANGELOG.md` describes the release.
- Confirm examples contain no real Moodle URLs, tokens, course names, grades, submissions, or user data.
- Confirm `moodle-mcp doctor` still gives actionable setup guidance.
- Tag with `vMAJOR.MINOR.PATCH`.
- Confirm GitHub Actions published via PyPI Trusted Publishing.
- Confirm release artifacts have GitHub artifact attestations.
