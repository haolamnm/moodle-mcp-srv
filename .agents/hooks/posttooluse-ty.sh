#!/usr/bin/env bash
set -euo pipefail

payload=$(cat)
file_path=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // ""')

if ! printf '%s' "$file_path" | grep -qE '\.py$'; then
  exit 0
fi

if [ ! -f "$file_path" ]; then
  exit 0
fi

# Single-pyproject project — repo root is always the right cwd.
root=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
rel=$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$file_path" "$root")

output=$(cd "$root" && uv run ty check "$rel" --output-format concise 2>&1) || true

if [ -z "$output" ]; then
  exit 0
fi

count=$(printf '%s' "$output" | grep -cE '^[^ ]+:[0-9]+:[0-9]+:' || true)

jq -n --arg output "$output" --arg count "$count" --arg file "$file_path" '{
  systemMessage: ("ty: found " + $count + " type issue(s) in " + $file),
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: ("=== PostToolUse hook: ty ===\ninfo: blazing-fast Python type checker → correctness you can trust\nwarning: found " + $count + " type issue(s) in " + $file + "\n" + $output + "\n\nFix these before continuing.")
  }
}'
