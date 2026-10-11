"""Warnings for the bootstrap output: technique cards (atoms), the reference map and the pitch files.

The bootstrap prompt asks the agent for atoms with a fixed shape (authoring/references/CARD-TEMPLATE.md) and for pitch
rounds with a fixed shape (PITCH-PROMPT.md). These checks make that shape mechanical, so the lint feedback after a write
tells the agent where a card or a pitch file falls short. They are warnings: never an import error. A card is a `##`
section with a `- Id:` line; older cards without one are not checked.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from .issues import Issue
from .policy import Policy, load_policy
from .textio import fold, read_text, slug

REFS = "authoring/references"
CARD_FIELDS = ("Id", "Binding", "Effect", "Mechanism", "Test", "In this world", "Plain", "Applied", "Avoid", "Evidence", "Used by")
_ATOM_ID = re.compile(r"^[a-z0-9][a-z0-9-]*\.[a-z][a-z-]*\.\d+$")
REVIEW_FIELDS = ("Status", "Review note")  # written by the review page (or the agent); not required by the lint
_FIELD = re.compile(r"^- (%s):\s*(.*)$" % "|".join(re.escape(f) for f in CARD_FIELDS + REVIEW_FIELDS))


_slug = slug


def _cards(text: str) -> list[tuple[str, dict[str, str]]]:
    """(heading, {field: value}) for each `##` section that has an Id line."""
    cards: list[tuple[str, dict[str, str]]] = []
    heading, fields, current = "", {}, ""
    def close() -> None:
        if "Id" in fields:
            cards.append((heading, fields))
    for line in text.split("\n"):
        if line.startswith("## "):
            close()
            heading, fields, current = line[3:].strip(), {}, ""
            continue
        match = _FIELD.match(line)
        if match:
            current = match.group(1)
            fields[current] = match.group(2).strip()
        elif current and line.strip() and not line.startswith(("#", "```")):
            fields[current] += " " + line.strip()  # a wrapped value
    close()
    return cards


def check_cards(root: Path, policy: Policy | None = None) -> tuple[list[Issue], set[str], int]:
    """Card issues, the set of atom id prefixes found, and how many cards there are."""
    policy = policy or load_policy(root)
    required, max_words = policy["lint.card_required_fields"], policy["lint.card_sample_max_words"]
    issues: list[Issue] = []
    prefixes: set[str] = set()
    total = 0
    for folder in ("roles", "categories"):
        base = root / REFS / folder
        if not base.is_dir():
            continue
        for path in sorted(base.glob("*.md")):
            where = f"{REFS}/{folder}/{path.name}"
            seen: set[str] = set()
            for heading, fields in _cards(read_text(path)):
                total += 1
                label = f"card `{heading}`"
                idline = fields.get("Id", "")
                atom_id = (re.match(r"(\S+)", idline) or re.match(r"()", "")).group(1)
                found = re.search(r"Binding:\s*(\w+)", idline)
                binding = (found.group(1) if found else fields.get("Binding", "")).strip().lower()
                missing = [f for f in required if f not in ("Id", "Binding") and not fields.get(f)]
                if missing:
                    issues.append(Issue("warning", "L-CARD-FIELD", where, f"{label} is missing: {', '.join(missing)}"))
                if not _ATOM_ID.match(atom_id):
                    issues.append(Issue("warning", "L-CARD-ID", where, f"{label}: the id `{atom_id}` should look like `<creator>.<aspect>.<n>`"))
                elif atom_id in seen:
                    issues.append(Issue("warning", "L-CARD-ID", where, f"{label}: the id `{atom_id}` appears twice in this file"))
                else:
                    seen.add(atom_id)
                    prefixes.add(atom_id.split(".")[0])
                if binding not in ("hard", "soft"):
                    issues.append(Issue("warning", "L-CARD-BINDING", where, f"{label}: Binding must be `hard` or `soft`, got `{binding or 'nothing'}`"))
                for sample in ("Plain", "Applied"):
                    words = len(fields.get(sample, "").split())
                    if words > max_words:
                        issues.append(Issue("warning", "L-CARD-SAMPLE", where, f"{label}: the {sample} sample is {words} words; keep each sample under about {max_words}"))
    return issues, prefixes, total


def _hard_references(root: Path) -> list[str]:
    try:
        data = json.loads(read_text(root / ".world-design" / "world.json"))
    except (OSError, ValueError):
        return []
    return [str(r.get("creator", "")) for r in data.get("references", []) if isinstance(r, dict) and r.get("binding") == "hard" and r.get("creator")]


def _covers(creator: str, prefixes: set[str]) -> bool:
    tokens = set(re.findall(r"[a-z0-9]+", fold(creator))) | {_slug(creator)}
    return any(p in tokens or _slug(creator).startswith(p) for p in prefixes)


def check_pitches(root: Path, hard: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    base = root / "design" / "pitches"
    if not base.is_dir():
        return issues
    for path in sorted(base.glob("round-*.md")):
        where = f"design/pitches/{path.name}"
        text = read_text(path)
        letters = {m.group(1).upper() for m in re.finditer(r"(?mi)^#{1,4}\s*(?:pitch\s+)?([A-D])\b", text)}
        absent = [x for x in "ABCD" if x not in letters]
        if absent:
            issues.append(Issue("warning", "L-PITCH-SHAPE", where, f"a round needs pitches A, B, C and a D wild card as headings; missing: {', '.join(absent)}"))
        if not re.search(r"(?i)recommend", text):
            issues.append(Issue("warning", "L-PITCH-SHAPE", where, "a round ends with the agent's recommendation and what it would not choose"))
        if hard and len(re.findall(r"(?i)hard references?:", text)) < len(letters):
            issues.append(Issue("warning", "L-PITCH-SHAPE", where, "each pitch needs a `Hard references:` line saying how every hard reference shows or why it cannot"))
    return issues


def check_references(root: Path, policy: Policy | None = None) -> list[Issue]:
    policy = policy or load_policy(root)
    issues, prefixes, total = check_cards(root, policy)
    if total and not (root / REFS / "ANALYSIS.md").is_file():
        issues.append(Issue("warning", "L-REF-MAP", f"{REFS}/ANALYSIS.md", "cards exist but there is no ANALYSIS.md with the reference map the user approves"))
    hard = _hard_references(root)
    if total:
        for creator in hard:
            if not _covers(creator, prefixes):
                issues.append(Issue("warning", "L-REF-HARD", f"{REFS}/", f"hard reference {creator} has no atom card (ids start with its name, `<creator>.<aspect>.<n>`)"))
    return issues + check_pitches(root, hard) + check_systems(root, policy) + check_voice(root, policy) + check_exemplars(root)


# --- game systems specs (design/systems/*.md): prose only, no balance numbers -----------------------------------------
@lru_cache(maxsize=8)
def _balance_regex(patterns: tuple[str, ...]) -> re.Pattern[str]:
    return re.compile(r"(?i)\b(" + "|".join(patterns) + r")\b|%")


_NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\w.]*\.md)")
_LIST_MARKER = re.compile(r"^\s*(?:[-*]\s*)?\d+[.)]\s+")
_ALLOWED = re.compile(r"(?i)user-given|\]\([a-z0-9-]+\.md[^)]*\)|::[a-z0-9-]+::")


def check_systems(root: Path, policy: Policy | None = None) -> list[Issue]:
    """`L-SYSTEM-NUMBERS`: a line of a game systems spec that states a value next to a balance word. A number taken from a
    world page (the line links to the page) or given by the user (`user-given:`) is allowed."""
    balance = _balance_regex(tuple((policy or load_policy(root))["lint.balance_patterns"]))
    issues: list[Issue] = []
    base = root / "design" / "systems"
    if not base.is_dir():
        return issues
    for path in sorted(base.glob("*.md")):
        if path.name.startswith("_"):
            continue
        in_fence = False
        for number, raw in enumerate(read_text(path).split("\n"), start=1):
            if raw.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            line = _LIST_MARKER.sub("", raw)
            if in_fence or line.lstrip().startswith("#") or _ALLOWED.search(line):
                continue
            if balance.search(line) and _NUMBER.search(line):
                issues.append(Issue("warning", "L-SYSTEM-NUMBERS", f"design/systems/{path.name}:{number}",
                                    "a systems spec states no balance numbers; describe the amount in words (scarce, a few uses before rest), "
                                    "or mark a value the user gave with `user-given:` or link the world page it comes from"))
    return issues


# --- voice.md and the exemplar passages ------------------------------------------------------------------------------
_EXAMPLE = re.compile(r"(?im)(\bexamples?\b|^>|^```|\"[^\"\n]{12,}\"|“[^”\n]{12,}”)")


def _sections(text: str) -> dict[str, str]:
    out: dict[str, list[str]] = {}
    current = ""
    for line in text.split("\n"):
        if line.startswith("## "):
            current = line[3:].strip().lower()
            out[current] = []
        elif current:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def check_voice(root: Path, policy: Policy | None = None) -> list[Issue]:
    """Once voice.md has been written (its status is no longer `not yet written`): a status line, the four sections, each with a rule and an example."""
    path = root / "voice.md"
    if not path.is_file():
        return []
    text = read_text(path)
    head = text.split("\n")[:12]
    status = next((re.match(r"(?i)^\s*status:\s*(.+?)\s*$", l).group(1).lower() for l in head if re.match(r"(?i)^\s*status:", l)), "")
    if status.startswith("not yet"):
        return []
    issues: list[Issue] = []
    if not status:
        issues.append(Issue("warning", "L-VOICE-STATUS", "voice.md", "no `Status:` line near the top: write `Status: proposed`; the user approves it by changing it to `Status: approved`"))
    sections = _sections(text)
    for wanted in (policy or load_policy(root))["lint.voice_sections"]:
        body = next((v for k, v in sections.items() if wanted in k), None)
        if body is None or len(body.split()) < 15:
            issues.append(Issue("warning", "L-VOICE-SECTION", "voice.md", f"the `{wanted}` section is missing or has no concrete rules"))
        elif not _EXAMPLE.search(body):
            issues.append(Issue("warning", "L-VOICE-EXAMPLE", "voice.md", f"the `{wanted}` section has no worked example (a quoted line, a blockquote, a code block, or the word Example)"))
    return issues


def _source_names(root: Path) -> list[str]:
    try:
        data = json.loads(read_text(root / ".world-design" / "world.json"))
    except (OSError, ValueError):
        return []
    names: set[str] = set()
    for ref in data.get("references", []):
        if not isinstance(ref, dict):
            continue
        creator, work = str(ref.get("creator", "")).strip(), str(ref.get("work", "")).strip()
        if len(creator) >= 4:
            names.add(creator)
            last = creator.split()[-1]
            if len(last) >= 5:
                names.add(last)
        if len(work) >= 4:
            names.add(work)
    return sorted(names)


def check_exemplars(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    base = root / REFS / "exemplars"
    if not base.is_dir():
        return issues
    names = _source_names(root)
    for path in sorted(base.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        where = f"{REFS}/exemplars/{path.name}"
        text = read_text(path)
        head = "\n".join(text.split("\n")[:8]).lower()
        missing = [k for k in ("status", "role", "purpose") if not re.search(rf"(?m)^{k}:", head)]
        if missing:
            issues.append(Issue("warning", "L-EXEMPLAR-HEADER", where, f"the first lines need {', '.join(f'`{k}:`' for k in missing)}"))
        body = text.lower()
        used = [n for n in names if n.lower() in body]
        if used:
            issues.append(Issue("warning", "L-EXEMPLAR-IMITATION", where, f"mentions {', '.join(used)}: an exemplar is original to this world and never uses a source's names, scenes or phrasing"))
    return issues
