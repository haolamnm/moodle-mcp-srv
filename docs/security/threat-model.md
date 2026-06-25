# Threat Model

This project is a local MCP server for Moodle Web Service access. Moodle remains the source of truth for authentication and authorization.

## Assets

- Moodle Web Service tokens.
- Course, assignment, quiz, forum, calendar, grade, submission, and user data returned by Moodle.
- Local logs, traces, test fixtures, and MCP client configuration.

## Boundaries

- The server talks to a configured Moodle REST endpoint.
- MCP clients can see data returned by tools and resources.
- HTTP transport is local-development oriented unless protected by external authentication and reverse-proxy controls.
- Moodle Feature checks are advisory setup diagnostics, not an authorization system.

## Threats

| Threat | Risk | Mitigations |
|---|---|---|
| Token leakage | Moodle tokens in config, logs, issue reports, shell history, or MCP client files can grant Moodle access. | Use `SecretStr`, redact logs, ignore local client config, keep examples placeholder-only, run Gitleaks, and report leaks privately. |
| Prompt injection through Moodle content | Course content, forum posts, assignment text, or feedback can include instructions that try to redirect the agent. | Treat Moodle content as untrusted data, keep tool descriptions explicit, prefer read-only resources for context, and require confirmation for writes. |
| Accidental write actions | Agents may submit assignments or post forum content when the user wanted a preview. | Write tools default to dry-run previews, require `reason` for real writes, and return write receipts. |
| HTTP transport exposure | Public HTTP transport can expose Moodle-backed tools to other users or networks. | Bind to `127.0.0.1` by default and do not expose HTTP publicly without external authentication, TLS, and reverse-proxy controls. |
| Log or fixture leakage | Live Moodle data in tests, logs, screenshots, or issues can expose private education records. | Keep live tests opt-in, use generic fixtures, redact bug reports, and never commit live Moodle logs or fixtures. |
| Malicious Moodle responses | A compromised or hostile Moodle instance can return oversized, malformed, or adversarial payloads. | Validate typed responses at boundaries, bound list sizes where tools support `limit`, and convert Moodle errors into safe tool errors. |
| Agent overreach against student data | Broad tool chains can retrieve more data than the user intended. | Prefer intent-level tools, use `course_ids` and `limit` filters, document least-privilege tokens, and keep permission-aware UX advisory. |

## Reporting

Use GitHub private vulnerability reporting for token exposure, private Moodle data leakage, authorization bypasses, or unsafe write behavior.
