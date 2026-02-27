#!/usr/bin/env bash
#
# Link built skills from dist/ into ~/.claude/skills/
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

DIST_SKILLS="$PROJECT_ROOT/dist/.claude/skills"
DEST_SKILLS="$HOME/.claude/skills"

if [ ! -d "$DIST_SKILLS" ]; then
    echo "Error: dist not found at $DIST_SKILLS"
    echo "Run 'make build' first."
    exit 1
fi

mkdir -p "$DEST_SKILLS"

for skill_dir in "$DIST_SKILLS"/*/; do
    skill_name="$(basename "$skill_dir")"
    link_target="$DEST_SKILLS/$skill_name"

    if [ -L "$link_target" ]; then
        rm "$link_target"
    elif [ -d "$link_target" ]; then
        echo "Warning: $link_target exists and is not a symlink, skipping."
        continue
    fi

    ln -s "$skill_dir" "$link_target"
    echo "Linked: $link_target -> $skill_dir"
done

echo "Done. Skills linked to $DEST_SKILLS"
