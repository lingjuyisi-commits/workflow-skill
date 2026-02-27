#!/usr/bin/env bash
#
# Watch skills/ for changes and auto-rebuild.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_ROOT/skills"

do_build() {
    echo ""
    echo "==> Change detected, rebuilding..."
    cd "$PROJECT_ROOT" && python3 -m adapters.build
}

echo "==> Initial build..."
cd "$PROJECT_ROOT" && python3 -m adapters.build

if command -v inotifywait &>/dev/null; then
    echo "==> Watching skills/ with inotifywait (Ctrl+C to stop)..."
    while inotifywait -r -e modify,create,delete "$SKILLS_DIR" 2>/dev/null; do
        do_build
    done
else
    echo "==> Watching skills/ with polling (Ctrl+C to stop)..."
    LAST_HASH=""
    while true; do
        CURRENT_HASH=$(find "$SKILLS_DIR" -type f -exec md5sum {} \; 2>/dev/null | sort | md5sum)
        if [ "$CURRENT_HASH" != "$LAST_HASH" ] && [ -n "$LAST_HASH" ]; then
            do_build
        fi
        LAST_HASH="$CURRENT_HASH"
        sleep 2
    done
fi
