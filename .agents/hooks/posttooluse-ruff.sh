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

# Run ruff and strip ANSI escape codes so the count regex and context are clean.
raw_output=$(cd "$root" && ruff check "$rel" 2>&1) || true
output=$(printf '%s' "$raw_output" | sed $'s/\x1b\\[[0-9;]*m//g')

if [ -z "$output" ]; then
  exit 0
fi

count=$(printf '%s' "$output" | grep -cE '^[A-Z]+[0-9]+ ' || true)

jq -n --arg output "$output" --arg count "$count" --arg file "$file_path" '{
  systemMessage: ("ruff: found " + $count + " issue(s) in " + $file),
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: ("=== PostToolUse hook: ruff ===\ninfo: best Python linter → fast, clean code\nwarning: found " + $count + " issue(s) in " + $file + "\n" + $output + "\n\nFix these before continuing.")
  }
}'
