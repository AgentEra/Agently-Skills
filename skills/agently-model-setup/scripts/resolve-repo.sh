#!/usr/bin/env bash
set -euo pipefail

candidate="${1:-${AGENTLY_REPO:-}}"

is_agently_repo() {
  local dir="$1"
  [ -n "$dir" ] || return 1
  [ -d "$dir" ] || return 1
  [ -f "$dir/pyproject.toml" ] || return 1
  [ -d "$dir/agently" ] || return 1
  return 0
}

walk_up() {
  local dir="$1"
  while [ "$dir" != "/" ]; do
    if is_agently_repo "$dir"; then
      printf '%s\n' "$dir"
      return 0
    fi
    dir="$(cd "$dir/.." && pwd)"
  done
  return 1
}

if [ -n "$candidate" ] && is_agently_repo "$candidate"; then
  cd "$candidate"
  pwd
  exit 0
fi

if walk_up "$(pwd)"; then
  exit 0
fi

echo "Agently repository not found. Pass a repo path or set AGENTLY_REPO." >&2
exit 1
