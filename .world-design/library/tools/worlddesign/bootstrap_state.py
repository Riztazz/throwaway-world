"""Where a world stands in its bootstrap: what is written, what waits for the user's approval, and whether the pitch round may start.

Read-only and derived from the files (the intake in `.world-design/world.json`, `authoring/references/`, `voice.md`, the
decisions). The agent proposes everything with `status: proposed`; the user approves by changing it to `approved`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .ledger import load_decisions
from .refcheck import REFS, _cards
from .textio import read_text

GAMES = ("online-game", "single-player-game")
PROSE_ROLES = ("fiction-writer", "narrative-editor")


def _read_json(path: Path) -> dict:
    try:
        data = json.loads(read_text(path))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def required_roles(root: Path, products: list[str]) -> list[str]:
    for base in (root / ".world-design" / "library", Path(__file__).resolve().parents[2]):
        data = _read_json(base / "agents" / "reference-categories.json")
        if data.get("required_roles"):
            roles = [str(r) for r in data["required_roles"]]
            return [r for r in roles if not (products and not any(p in GAMES for p in products) and r == "quest-narrative-designer")]
    return []


def _status(text: str) -> str:
    """The first `status:` value in the first lines of a file (frontmatter or a plain line), lowercased; '' when none."""
    for line in text.split("\n")[:12]:
        match = re.match(r"(?i)^\s*status:\s*(.+?)\s*\.?\s*$", line)
        if match:
            value = match.group(1).lower()
            return "missing" if value.startswith("not yet") else value.split()[0]
    return ""


def build_state(root: Path) -> tuple[str, list[str]]:
    """(report text, blockers). No blockers means the pitch round may start."""
    world = _read_json(root / ".world-design" / "world.json")
    intake = world.get("intake") if isinstance(world.get("intake"), dict) else {}
    refs = [r for r in world.get("references", []) if isinstance(r, dict)]
    products = [p for p in (intake.get("products") or []) if isinstance(p, str)]
    blockers: list[str] = []
    lines = [f"BOOTSTRAP STATUS: {world.get('name') or root.name}"]

    hard = sum(1 for r in refs if r.get("binding") == "hard")
    lines.append(f"1. Intake: products {', '.join(products) or 'none ticked'}; {len(refs)} reference(s), {hard} hard.")
    accepted = open_q = 0
    for d in load_decisions(root):
        if d.error:
            continue
        accepted += d.meta.get("status") == "accepted"
        open_q += d.meta.get("status") in ("open", "proposed")
    lines.append(f"2. Decisions: {accepted} accepted, {open_q} open or proposed.")

    analysis = root / REFS / "ANALYSIS.md"
    state = _status(read_text(analysis)) if analysis.is_file() else "missing"
    lines.append(f"3. Reference map (ANALYSIS.md): {state or 'no status line'}.")
    if state != "approved":
        blockers.append("approve the reference map: set `status: approved` in authoring/references/ANALYSIS.md" if analysis.is_file()
                        else "the reference map (authoring/references/ANALYSIS.md) is not written yet: run the bootstrap prompt")

    cards = {"hard": 0, "soft": 0, "other": 0}
    carded: set[str] = set()
    for folder in ("roles", "categories"):
        base = root / REFS / folder
        for path in sorted(base.glob("*.md")) if base.is_dir() else []:
            for _, fields in _cards(read_text(path)):
                bind = (re.search(r"Binding:\s*(\w+)", fields.get("Id", "")) or re.match(r"()", "")).group(1).lower() or fields.get("Binding", "").lower()
                cards[bind if bind in ("hard", "soft") else "other"] += 1
                if folder == "roles":
                    carded.add(path.stem)
    lines.append(f"4. Atom cards: {cards['hard']} hard, {cards['soft']} soft" + (f", {cards['other']} without a binding" if cards["other"] else "") + ".")
    missing = [r for r in required_roles(root, products) if not (root / REFS / "roles" / f"{r}.md").is_file()]
    if missing:
        lines.append(f"   Required roles without a role card: {', '.join(missing)}.")
        blockers.append(f"write role cards for: {', '.join(missing)}")

    voice = root / "voice.md"
    vstate = _status(read_text(voice)) if voice.is_file() else "missing"
    lines.append(f"5. voice.md: {vstate or 'no status line'}.")
    if vstate != "approved":
        blockers.append("approve voice.md: set `Status: approved` at the top" if vstate in ("proposed", "draft") else "voice.md is not written yet: run the bootstrap prompt")

    ex_dir = root / REFS / "exemplars"
    exemplars = [p for p in sorted(ex_dir.glob("*.md")) if p.name.lower() != "readme.md"] if ex_dir.is_dir() else []
    states = {p.name: _status(read_text(p)) for p in exemplars}
    approved = [n for n, s in states.items() if s == "approved"]
    lines.append(f"6. Exemplars: {len(approved)} approved, {len(exemplars) - len(approved)} proposed.")
    if exemplars and not approved:
        blockers.append("approve at least one exemplar: set `status: approved` in a file under authoring/references/exemplars/")
    if not exemplars:
        blockers.append("no exemplar passages yet: run the bootstrap prompt")

    rounds = sorted((root / "design" / "pitches").glob("round-*.md")) if (root / "design" / "pitches").is_dir() else []
    lines.append(f"7. Pitch rounds written: {len(rounds)}.")
    lines.append("")
    if blockers:
        lines.append("NOT READY for the pitch round. Still to do:")
        lines += [f"  - {b}" for b in blockers]
    else:
        lines.append("READY for the pitch round: paste PITCH-PROMPT.md in a fresh session.")
    return "\n".join(lines), blockers
