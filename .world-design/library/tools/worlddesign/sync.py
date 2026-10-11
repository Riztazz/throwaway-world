"""Generate native Codex and Claude Code adapters from the shared role definitions.

Port of the retired Node sync script. Check mode only reads; write mode preflights every collision
before changing generated adapters, and never deletes leftovers.
"""

from __future__ import annotations

import json
from pathlib import Path

from .render import (
    claude_definition,
    codex_definition,
    generated_adapter,
    native_name,
    parse_registry,
    profile_prompt,
    resolve_effort,
    resolve_model,
)
from .textio import read_text, write_text

ADAPTER_FOLDERS = (".codex/agents", ".claude/agents")


def render_adapters(library_root: Path | str, exclude_roles: frozenset[str] = frozenset(),
                    preload_skills: bool = False, models_override: dict | None = None) -> dict[str, str]:
    """All native adapters for a library (or a library snapshot) as {relative path: content}.

    `exclude_roles` leaves roles (and their skills) out, for worlds created without an optional pack.
    `preload_skills` adds the Claude `skills:` list; it needs the skills installed under .claude/skills,
    which a world has and the library itself does not. `models_override` is a world's models.json.
    """
    root = Path(library_root)
    source = root / "agents"
    all_profiles = parse_registry(json.loads(read_text(source / "registry.json")))
    profiles = [p for p in all_profiles if p.id not in exclude_roles]
    models = json.loads(read_text(source / "models.json")) if (source / "models.json").is_file() else {}
    dropped_skills = {s for p in all_profiles if p.id in exclude_roles for s in p.skills}
    contract = read_text(source / "contract.md")
    skills_root = root / "skills"
    available = {
        entry.name for entry in skills_root.iterdir() if entry.is_dir() and (entry / "SKILL.md").exists()
    } - dropped_skills
    assigned = {skill for profile in profiles for skill in profile.skills}
    if available != assigned:
        raise ValueError("Narrative registry must assign each existing design skill exactly once")

    outputs: dict[str, str] = {}
    for profile in profiles:
        prompt = profile_prompt(profile, contract, read_text(source / profile.path))
        stem = native_name(profile.id)
        outputs[f".codex/agents/{stem}.toml"] = codex_definition(
            profile, prompt, resolve_model(models, models_override, "codex", profile.tier),
            resolve_effort(models, models_override, "codex", profile.tier, profile.id))
        outputs[f".claude/agents/{stem}.md"] = claude_definition(
            profile, prompt, resolve_model(models, models_override, "claude", profile.tier), preload_skills,
            resolve_effort(models, models_override, "claude", profile.tier, profile.id))
    return outputs


def sync_narrative_agents(root: Path | str, write: bool = False) -> int:
    root = Path(root)
    profiles = parse_registry(json.loads(read_text(root / "agents" / "registry.json")))
    outputs = render_adapters(root)

    problems: list[str] = []
    changes: list[tuple[str, str]] = []
    for rel, content in outputs.items():
        full = root / rel
        before = read_text(full) if full.exists() else None
        if before is not None and not generated_adapter(rel, before):
            problems.append(f"Non-generated adapter collision: {rel}")
        elif before != content:
            changes.append((rel, content))
    for folder in ADAPTER_FOLDERS:
        directory = root / folder
        if not directory.is_dir():
            continue
        for entry in sorted(p.name for p in directory.iterdir()):
            rel = f"{folder}/{entry}"
            if entry.startswith("narrative-") and rel not in outputs:
                problems.append(f"Obsolete adapter needs review: {rel}")
    if problems:
        raise ValueError("\n".join(problems))
    if not write and changes:
        raise ValueError("Narrative adapter drift:\n" + "\n".join(rel for rel, _ in changes))
    if write:
        for rel, content in changes:
            write_text(root / rel, content)
    return len(profiles)


MODE_SKILL = "templates/world/.claude/skills/world-mode/SKILL.md"


def sync_mode_skill(root: Path | str, write: bool = False) -> bool:
    """Keep the mode list in the /world-mode skill equal to the table in worlddesign/mode.py. True when it was out of date
    (in write mode it has been rewritten)."""
    from .mode import SKILL_LIST_END, SKILL_LIST_START, render_mode_list
    path = Path(root) / MODE_SKILL
    text = read_text(path)
    start, end = text.find(SKILL_LIST_START), text.find(SKILL_LIST_END)
    if start < 0 or end < start:
        raise ValueError(f"{MODE_SKILL} has no {SKILL_LIST_START} ... {SKILL_LIST_END} block for the generated mode list")
    fresh = text[:start] + render_mode_list() + text[end + len(SKILL_LIST_END):]
    if fresh == text:
        return False
    if write:
        write_text(path, fresh)
    return True
