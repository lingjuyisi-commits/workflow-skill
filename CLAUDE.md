# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Does

A build pipeline for developing **Claude Code / OpenClaw skills**. Source files in `skills/` are compiled into `SKILL.md` files (with YAML frontmatter) deployed to `~/.claude/skills/<name>/`.

## Commands

```bash
make build       # Build all skills → dist/
make link        # Build + symlink dist/ to ~/.claude/skills/
make test        # Run pytest tests
make watch       # Watch skills/ for changes and auto-rebuild
make publish     # Build + copy to published/ (for distribution)
make clean       # Remove dist/
```

Build a single skill:
```bash
python3 -m adapters.build --skill commit
```

Run a single test file:
```bash
python3 -m pytest tests/test_adapters.py -v
```

**Requirements:** Python 3.6+, PyYAML (`pip install pyyaml`), pytest

## Architecture

### Source → Build → Publish → Distribute

```
skills/<name>/
  skill.yaml     # Metadata (frontmatter fields + source-only fields)
  prompt.md      # Raw prompt content
  [companions]   # Any other files (scripts/, examples.md, etc.) copied as-is
```

The build pipeline (`adapters/build.py` → `adapters/claude_code.py`) reads each skill directory and produces:

```
dist/.claude/skills/<name>/SKILL.md   # frontmatter + prompt, gitignored
published/.claude/skills/<name>/      # committed release snapshot
```

`install.sh` (pure bash) lets users install from `published/` without Python.

### skill.yaml Fields

Fields written to `SKILL.md` frontmatter (`FRONTMATTER_FIELDS` in `claude_code.py`):
- `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools`
- `disable-model-invocation`, `model`, `context`, `agent`, `hooks`

Fields that are **source-only** (excluded from output): `version`, `tags`

### Adding a New Skill

1. Create `skills/<name>/skill.yaml` and `skills/<name>/prompt.md`
2. Run `make build` — output appears in `dist/.claude/skills/<name>/SKILL.md`
3. Use `make link` to test locally in Claude Code
4. Run `make publish` and commit `published/` to distribute to users

Companion files (anything in the skill directory besides `skill.yaml` and `prompt.md`) are copied verbatim into the build output.

### Tests

Tests live in `tests/test_adapters.py` and use fixture skill directories in `tests/fixtures/`. They test `generate_frontmatter()`, `generate_skill_md()`, and `build_skill()` from `adapters/claude_code.py`.
