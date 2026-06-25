# MCP Client Examples

These examples avoid embedding Moodle tokens in committed config.

Prefer OS environment variables or the client secret store when supported. Do not commit real Moodle tokens or private site URLs.

## Clients

- VS Code: `vscode.mcp.json`
- Zed: `zed.settings.json`
- Claude Desktop: `claude-desktop.json`
- Claude Code: `claude-code.mcp.json`
- Codex: `codex.config.toml`
- Gemini CLI: `gemini.settings.json`
- OpenCode: `opencode.json`
- Factory Droid: `droid.mcp.json`, `droid.md`
- Pi Code: `pi-code.mcp.json`

## Notes

- Stdio examples run `uvx --from moodle-mcp-srv moodle-mcp`.
- Set `MOODLE_API_URL` and `MOODLE_API_TOKEN` in the OS environment before starting the client, or use the client's secret/input mechanism.
- If a GUI client does not inherit shell environment variables, copy the example to a local ignored config file and add secrets there only.
- Restart or reload the client after changing MCP config.
