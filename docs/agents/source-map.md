# Agent Source Map

Use this map when an external dependency, CLI, or Moodle API detail may have changed.

## Sources

| Concern | Primary agent source | Fallback |
|---|---|---|
| FastMCP | https://gofastmcp.com/llms.txt | Use linked `.md` pages from that index. |
| MCP protocol | https://modelcontextprotocol.io/llms-full.txt | https://modelcontextprotocol.io/docs |
| Pydantic | https://pydantic.dev/llms.txt | https://pydantic.dev/docs/validation/latest/get-started/ |
| Ruff | https://docs.astral.sh/ruff/llms.txt | Use explicit `index.md` paths from that index. |
| uv | https://docs.astral.sh/uv/llms.txt | Use explicit `index.md` paths from that index. |
| ty | https://docs.astral.sh/ty/llms.txt | Use explicit `index.md` paths from that index. |
| Python 3.13 | https://docs.python.org/3.13/ | https://docs.python.org/3/whatsnew/3.13.html |
| Moodle Web Services | https://moodledev.io/docs/apis/subsystems/external | Use the target Moodle site's Web services API documentation when available. |
| Moodle API functions | https://docs.moodle.org/dev/Web_service_API_functions | Prefer the target Moodle site's function reference for exact enabled functions. |
| pytest | https://docs.pytest.org/en/stable/contents.html | Try `https://docs.pytest.org/en/stable/llms.txt`; it may be rate-limited. |
| Hypothesis | https://hypothesis.readthedocs.io/en/latest/ | Use for property-based tests of pure coercion, filtering, and parameter helpers. |
| structlog | https://www.structlog.org/en/stable/ | https://www.structlog.org/en/stable/standard-library.html |
| Conventional Commits | https://www.conventionalcommits.org/en/v1.0.0/ | `pyproject.toml` Commitizen config. |

## Fetching

- Prefer `llms.txt` when present.
- For Astral docs, use explicit `index.md` paths from the `llms.txt` index.
- For Moodle function behavior, prefer the target Moodle site's Web services API documentation over generic Moodle docs.
