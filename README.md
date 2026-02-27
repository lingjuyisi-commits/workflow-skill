# my-skills

A unified repository for developing and managing skills for **Claude Code** and **OpenClaw**.

Both tools use the same format (`.claude/skills/<name>/SKILL.md`), so a single adapter handles both targets.

## Repository Structure

```
skills/           # Source files (single source of truth)
  commit/
    skill.yaml    # Metadata (name, description, allowed-tools, etc.)
    prompt.md     # Core prompt content
adapters/         # Build pipeline
  build.py        # Main entry point
  claude_code.py  # SKILL.md generator
dist/             # Build output (gitignored)
tests/            # pytest tests
scripts/          # Dev utilities
Makefile          # Build commands
```

## Quick Start

```bash
# Build all skills for all targets
make build

# Build for a specific target
make build-claude
make build-openclaw

# Link built skills to ~/.claude/skills/
make link

# Run tests
make test

# Watch for changes and auto-rebuild
make watch

# Clean build output
make clean
```

## Adding a New Skill

1. Create a directory under `skills/`:
   ```
   skills/my-skill/
     skill.yaml
     prompt.md
   ```

2. Define metadata in `skill.yaml`:
   ```yaml
   name: my-skill
   description: "What the skill does"
   user-invocable: true
   allowed-tools:
     - Bash
     - Read
   ```

3. Write the prompt in `prompt.md`.

4. Run `make build` to generate `SKILL.md` files in `dist/`.

## skill.yaml Fields

| Field | Description |
|-------|-------------|
| `name` | Skill identifier |
| `description` | Short description |
| `argument-hint` | Hint shown for arguments (e.g., `"<pr-number>"`) |
| `user-invocable` | Whether users can invoke via `/<name>` |
| `allowed-tools` | List of tools the skill can use |
| `disable-model-invocation` | Prevent model from auto-invoking |
| `model` | Override model for this skill |
| `context` | Additional context configuration |
| `agent` | Agent configuration |
| `hooks` | Hook configuration |

Fields not in this list (e.g., `version`, `tags`) are for source management only and are excluded from the generated `SKILL.md`.

## Internal Distribution (for Users)

Install skills directly from this repository — no Python or PyYAML needed, just `git` and `bash`.

**One-time setup:**
```bash
git clone <repo-url> my-skills
```

**Install a skill:**
```bash
bash my-skills/install.sh                # list available skills
bash my-skills/install.sh commit         # install a specific skill
bash my-skills/install.sh all            # install all skills
```

**Stay up to date:**
```bash
bash my-skills/install.sh update         # git pull + reinstall all currently installed skills
```

Skills are installed to `~/.claude/skills/` and are immediately available in Claude Code.

---

## Maintainer: Publishing Skills

After editing skills, run:
```bash
make publish   # build + copy to published/
git add published/ && git commit -m "publish: update skills"
git push
```

Users get the update by running `bash install.sh update`.

---

## Requirements

- Python 3.6+
- PyYAML (`pip install pyyaml`)
- pytest (for testing)
