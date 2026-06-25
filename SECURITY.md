# Security Policy

## Supported Versions

This project is pre-1.0. Only the latest released version receives security fixes.

## Reporting Vulnerabilities

Do not open a public issue for token exposure, private Moodle data leaks, or authorization bypasses.

Use GitHub private vulnerability reporting:

```text
https://github.com/haolamnm/moodle-mcp-srv/security/advisories/new
```

Include the affected version or commit, reproduction steps, expected impact, and whether Moodle tokens, grades, submissions, or user data may be exposed.

## Security Boundaries

- Moodle remains the source of truth for authorization.
- Moodle Feature availability checks are advisory setup diagnostics, not a replacement for Moodle permissions.
- Use a least-privilege Moodle web-service token.
- Do not expose HTTP transport publicly without authentication and reverse-proxy controls.
- Do not commit `.env`, `.env.local`, Moodle tokens, private logs, live Moodle fixtures, grades, submissions, or student data.
- Write tools use dry-run previews by default and require a human-readable `reason` for real writes.
