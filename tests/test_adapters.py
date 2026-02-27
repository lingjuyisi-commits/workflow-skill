"""Tests for the skill adapter / build pipeline."""

import tempfile
from pathlib import Path

from adapters.claude_code import (
    build_skill,
    generate_frontmatter,
    generate_skill_md,
    load_skill,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestLoadSkill:
    def test_load_commit(self):
        skill = load_skill(FIXTURES_DIR / "commit")
        assert skill["metadata"]["name"] == "commit"
        assert "git commit" in skill["prompt"]

    def test_missing_yaml(self, tmp_path):
        (tmp_path / "prompt.md").write_text("hello")
        try:
            load_skill(tmp_path)
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_missing_prompt(self, tmp_path):
        (tmp_path / "skill.yaml").write_text("name: test")
        try:
            load_skill(tmp_path)
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass


class TestGenerateFrontmatter:
    def test_basic_fields(self):
        metadata = {"name": "test", "description": "A test skill", "user-invocable": True}
        fm = generate_frontmatter(metadata)
        assert fm.startswith("---")
        assert fm.endswith("---")
        assert "name: test" in fm
        assert "user-invocable: true" in fm

    def test_ignores_unknown_fields(self):
        metadata = {"name": "test", "version": "1.0.0", "tags": ["a"]}
        fm = generate_frontmatter(metadata)
        assert "name: test" in fm
        assert "version" not in fm
        assert "tags" not in fm

    def test_empty_metadata(self):
        fm = generate_frontmatter({})
        assert fm == ""


class TestGenerateSkillMd:
    def test_commit_fixture(self):
        result = generate_skill_md(FIXTURES_DIR / "commit")
        expected = (FIXTURES_DIR / "commit" / "expected.md").read_text()
        assert result == expected

    def test_has_frontmatter_and_prompt(self):
        result = generate_skill_md(FIXTURES_DIR / "commit")
        assert result.startswith("---")
        assert "git commit" in result


class TestBuildSkill:
    def test_build_creates_skill_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            result = build_skill(FIXTURES_DIR / "commit", output_dir)
            assert result.exists()
            assert result.name == "SKILL.md"
            assert ".claude/skills/commit" in str(result)
            content = result.read_text()
            assert "---" in content

    def test_build_output_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            build_skill(FIXTURES_DIR / "commit", output_dir)
            expected_dir = output_dir / ".claude" / "skills" / "commit"
            assert expected_dir.is_dir()
            assert (expected_dir / "SKILL.md").exists()
