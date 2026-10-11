"""Validate registry/skill metadata (port of validateSkills in scripts/check.ts)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .render import parse_registry
from .textio import read_text

_FRONT = re.compile(r"^---\n([\s\S]*?)\n---(?:\n|$)")


def validate_skills(root: Path | str) -> int:
    """Return the number of assigned base skills; raise ValueError on any problem."""
    root = Path(root)
    profiles = parse_registry(json.loads(read_text(root / "agents" / "registry.json")))
    skills_root = root / "skills"
    assigned = {skill for profile in profiles for skill in profile.skills}
    available = {entry.name for entry in skills_root.iterdir() if entry.is_dir()}
    if available != assigned:
        raise ValueError("Every top-level base skill must be assigned to exactly one registry role")

    for profile in profiles:
        role_path = root / "agents" / profile.path
        if not role_path.is_file():
            raise ValueError(f"Missing role brief: {profile.path}")
        role = read_text(role_path)
        for skill in profile.skills:
            rel = f"skills/{skill}/SKILL.md"
            text = read_text(root / rel)
            match = _FRONT.match(text)
            if not match:
                raise ValueError(f"Missing YAML frontmatter: {rel}")
            front = match.group(1)
            name = re.search(r"^name:\s*(\S+)\s*$", front, re.M)
            description = re.search(r"^description:\s*(.*?)\s*$", front, re.M)
            if not name or name.group(1) != skill:
                raise ValueError(f"Skill name must match its directory ({skill}): {rel}")
            desc = description.group(1) if description else ""
            if len(desc) < 40 or len(desc) > 300 or not re.match(r"^Use when\b", desc, re.I):
                raise ValueError(f"Skill description must be meaningful and 40-300 characters: {rel}")
            if skill not in role or rel not in role:
                raise ValueError(f"Role brief must list its assigned skill and entrypoint: {profile.id} -> {rel}")
    return len(assigned)
