#!/usr/bin/env python3
"""
Main build script: iterate over skills/ and generate dist/ outputs.

Usage:
    python -m adapters.build [--skill <name>]
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from adapters.claude_code import build_skill

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
DIST_DIR = PROJECT_ROOT / "dist"


def discover_skills(skills_dir: Path, skill_filter: Optional[str] = None) -> List[Path]:
    """Find all skill directories (or a single one if filtered)."""
    if skill_filter:
        skill_path = skills_dir / skill_filter
        if not skill_path.is_dir():
            print("Error: skill '{}' not found in {}".format(skill_filter, skills_dir), file=sys.stderr)
            sys.exit(1)
        return [skill_path]

    return sorted(p for p in skills_dir.iterdir() if p.is_dir() and (p / "skill.yaml").exists())


def build(skill_filter: Optional[str] = None):
    """Build skills to dist/."""
    skill_dirs = discover_skills(SKILLS_DIR, skill_filter)

    if not skill_dirs:
        print("No skills found.", file=sys.stderr)
        sys.exit(1)

    print("==> Building skills...")
    for skill_dir in skill_dirs:
        result = build_skill(skill_dir, DIST_DIR)
        print("    {} -> {}".format(skill_dir.name, result.relative_to(PROJECT_ROOT)))

    print("\nDone. Built {} skill(s).".format(len(skill_dirs)))


def main():
    parser = argparse.ArgumentParser(description="Build skills")
    parser.add_argument("--skill", default=None, help="Build a single skill by name")
    args = parser.parse_args()
    build(args.skill)


if __name__ == "__main__":
    main()
