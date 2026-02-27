"""
Generate SKILL.md files from skill.yaml + prompt.md sources.

Works for both Claude Code and OpenClaw since the format is identical:
  .claude/skills/<name>/SKILL.md
"""

import yaml
from pathlib import Path

# Fields from skill.yaml that map directly to SKILL.md frontmatter
FRONTMATTER_FIELDS = [
    "name",
    "description",
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "model",
    "context",
    "agent",
    "hooks",
]


def load_skill(skill_dir: Path) -> dict:
    """Load skill.yaml and prompt.md from a skill directory."""
    yaml_path = skill_dir / "skill.yaml"
    prompt_path = skill_dir / "prompt.md"

    if not yaml_path.exists():
        raise FileNotFoundError(f"Missing skill.yaml in {skill_dir}")
    if not prompt_path.exists():
        raise FileNotFoundError(f"Missing prompt.md in {skill_dir}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    return {"metadata": metadata, "prompt": prompt}


def generate_frontmatter(metadata: dict) -> str:
    """Convert skill metadata to YAML frontmatter string."""
    frontmatter = {}
    for field in FRONTMATTER_FIELDS:
        if field in metadata:
            frontmatter[field] = metadata[field]

    if not frontmatter:
        return ""

    lines = ["---"]
    lines.append(yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True).rstrip())
    lines.append("---")
    return "\n".join(lines)


def generate_skill_md(skill_dir: Path) -> str:
    """Generate SKILL.md content from a skill directory."""
    skill = load_skill(skill_dir)
    frontmatter = generate_frontmatter(skill["metadata"])
    prompt = skill["prompt"].rstrip()

    if frontmatter:
        return f"{frontmatter}\n\n{prompt}\n"
    else:
        return f"{prompt}\n"


def build_skill(skill_dir: Path, output_dir: Path) -> Path:
    """
    Build a single skill and write SKILL.md to the output directory.

    Returns the path to the generated SKILL.md.
    """
    skill_name = skill_dir.name
    target_dir = output_dir / ".claude" / "skills" / skill_name
    target_dir.mkdir(parents=True, exist_ok=True)

    content = generate_skill_md(skill_dir)
    skill_md_path = target_dir / "SKILL.md"
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Copy companion files (scripts/, examples.md, etc.)
    _copy_companions(skill_dir, target_dir)

    return skill_md_path


def _copy_companions(skill_dir: Path, target_dir: Path):
    """Copy companion files (anything except skill.yaml and prompt.md)."""
    import shutil

    skip = {"skill.yaml", "prompt.md"}
    for item in skill_dir.iterdir():
        if item.name in skip:
            continue
        dest = target_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
