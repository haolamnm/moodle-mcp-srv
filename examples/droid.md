# Factory Droid

Factory Droid can manage MCP servers through `/mcp` in the TUI or through its MCP config file.

For a config-file setup, adapt `droid.mcp.json` into:

```text
~/.factory/mcp.json
```

For an interactive setup, run Droid and use:

```sh
/mcp
```

Then add a custom stdio server:

```text
Name: moodle
Command: uvx
Args: --from moodle-mcp-srv moodle-mcp
Environment:
  leave empty if Droid inherits your OS environment, or set values only in your local untracked config
```

Use `/mcp list` to inspect connection status after setup.
