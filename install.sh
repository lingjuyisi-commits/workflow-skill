#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLISHED="$REPO_DIR/published/.claude/skills"
DEST="$HOME/.claude/skills"

# Extract description from SKILL.md frontmatter (no Python needed)
get_description() {
    local skill_md="$1/SKILL.md"
    [[ -f "$skill_md" ]] || { echo "(no description)"; return; }
    awk '/^---/{f=!f;next} f && /^description:/{
        sub(/^description:[[:space:]]*/,""); gsub(/^"|"$/,""); print; exit
    }' "$skill_md"
}

list_skills() {
    if [[ ! -d "$PUBLISHED" ]]; then
        echo "No published skills found at: $PUBLISHED" >&2
        exit 1
    fi
    echo "Available skills:"
    for skill_dir in "$PUBLISHED"/*/; do
        local name
        name="$(basename "$skill_dir")"
        local desc
        desc="$(get_description "$skill_dir")"
        printf "  %-20s %s\n" "$name" "$desc"
    done
}

install_skill() {
    local name="$1"
    local src="$PUBLISHED/$name"
    if [[ ! -d "$src" ]]; then
        echo "Error: skill '$name' not found in published skills." >&2
        echo "Run 'bash install.sh' to list available skills." >&2
        exit 1
    fi
    mkdir -p "$DEST"
    rm -rf "$DEST/$name"
    cp -r "$src" "$DEST/$name"
    echo "Installed: $name -> $DEST/$name"
}

install_all() {
    if [[ ! -d "$PUBLISHED" ]]; then
        echo "No published skills found at: $PUBLISHED" >&2
        exit 1
    fi
    local count=0
    for skill_dir in "$PUBLISHED"/*/; do
        local name
        name="$(basename "$skill_dir")"
        install_skill "$name"
        count=$((count + 1))
    done
    echo "Installed $count skill(s)."
}

do_update() {
    echo "Pulling latest changes..."
    git -C "$REPO_DIR" pull

    if [[ ! -d "$DEST" ]]; then
        echo "No skills currently installed (nothing to update)."
        return
    fi

    local count=0
    for installed_dir in "$DEST"/*/; do
        [[ -d "$installed_dir" ]] || continue
        local name
        name="$(basename "$installed_dir")"
        if [[ -d "$PUBLISHED/$name" ]]; then
            install_skill "$name"
            count=$((count + 1))
        else
            echo "Warning: '$name' is installed but no longer in published skills (skipped)."
        fi
    done
    echo "Updated $count skill(s)."
}

case "${1:-}" in
    "")
        list_skills
        ;;
    all)
        install_all
        ;;
    update)
        do_update
        ;;
    -h|--help)
        cat <<EOF
Usage: bash install.sh [COMMAND]

Commands:
  (none)          List available skills
  <skill-name>    Install a specific skill
  all             Install all skills
  update          git pull + reinstall already-installed skills
  -h, --help      Show this help

Examples:
  bash install.sh
  bash install.sh commit
  bash install.sh all
  bash install.sh update
EOF
        ;;
    *)
        install_skill "$1"
        ;;
esac
