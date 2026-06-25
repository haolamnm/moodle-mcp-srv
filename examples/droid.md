# Factory Droid

Register the stdio server with placeholder Moodle credentials:

```sh
droid mcp add moodle "uvx --from moodle-mcp-srv moodle-mcp" \
  --type stdio \
  --env MOODLE_API_URL=https://moodle.example.edu/webservice/rest/server.php \
  --env MOODLE_API_TOKEN=replace-me
```

Inside Droid, use `/mcp` to inspect the server and available tools.
