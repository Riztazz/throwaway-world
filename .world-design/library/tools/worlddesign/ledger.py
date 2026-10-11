"""Baselines, change records, decisions and the stale list (everything under ledger/ and decisions/)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .miniyaml import split_frontmatter
from .textio import read_text, write_text
from .world import World

BASELINE_REL = "ledger/page-hashes.json"
STALE_REL = "ledger/stale.md"
DECISION_STATUSES = ("open", "proposed", "accepted", "superseded", "rejected")
DECISION_TYPES = ("creative", "project", "question")
CHANGE_MODES = ("explore", "extend", "edit", "lock")
CHANGE_TIERS = ("T1b", "T2", "T3")
CHANGE_STATUSES = ("proposed", "integrated", "accepted", "rejected")


@dataclass
class Record:
    path: str  # relative to world root, forward slashes
    meta: dict[str, Any]
    error: str = ""


def load_baseline(root: Path) -> dict | None:
    path = root / BASELINE_REL
    if not path.is_file():
        return None
    data = json.loads(read_text(path))
    if data.get("version") != 1 or not isinstance(data.get("pages"), dict):
        raise ValueError(f"{BASELINE_REL}: unsupported baseline format")
    return data


def classify_changes(world: World, baseline: dict | None) -> dict[str, str]:
    """Map page file -> 'new' | 'changed' | 'deleted' | 'unchanged' against the baseline."""
    if baseline is None:
        return {f: "new" for f in world.pages}
    old = baseline["pages"]
    result = {}
    for file, page in world.pages.items():
        if file not in old:
            result[file] = "new"
        elif old[file]["sha256"] != page.sha256():
            result[file] = "changed"
        else:
            result[file] = "unchanged"
    for file in old:
        if file not in world.pages:
            result[file] = "deleted"
    return result


def _load_records(root: Path, folder: str, skip: tuple[str, ...]) -> list[Record]:
    out: list[Record] = []
    directory = root / folder
    if not directory.is_dir():
        return out
    for path in sorted(directory.glob("*.md")):
        if path.name in skip or path.name.startswith("_"):
            continue
        rel = f"{folder}/{path.name}"
        try:
            meta, _ = split_frontmatter(read_text(path))
            out.append(Record(rel, meta))
        except ValueError as error:
            out.append(Record(rel, {}, str(error)))
    return out


def load_decisions(root: Path) -> list[Record]:
    return _load_records(root, "decisions", ("INBOX.md", "INDEX.md", "README.md"))


def load_changes(root: Path) -> list[Record]:
    return _load_records(root, "ledger/changes", ())


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    return [str(v) for v in value] if isinstance(value, list) else [str(value)]


def record_pages(record: Record) -> set[str]:
    """The page files a change record lists (`harbour` and `harbour.md` both mean harbour.md)."""
    return {p if p.endswith(".md") else f"{p}.md" for p in as_list(record.meta.get("pages"))}


def consumed_records(baseline: dict | None) -> set[str]:
    """Paths of the T3 records a checkpoint has already spent (the baseline lists them; an older baseline lists none)."""
    return set(baseline.get("consumed", [])) if baseline else set()


def is_authorization(record: Record, baseline: dict | None = None) -> bool:
    """A T3 record with the user's words that has not been rejected and has not been spent by a checkpoint: the one thing that
    unlocks a protected page. A T3 record authorizes the change the user approved, not every later change to the page, so the
    snapshot that makes the change the new baseline also retires the record. The write guard and the lint use this one rule."""
    meta = record.meta
    return (not record.error and meta.get("tier") == "T3" and bool(str(meta.get("authority", "")).strip())
            and meta.get("status") != "rejected" and record.path not in consumed_records(baseline))


def consume_authorizations(root: Path, baseline: dict) -> dict:
    """Mark every T3 authorization that exists now as spent, in the baseline being written at a checkpoint."""
    spent = sorted(set(consumed_records(baseline)) | {r.path for r in load_changes(root) if is_authorization(r)})
    return {**baseline, "consumed": spent}


_STALE_LINE = re.compile(r"^- \[( |x)\] (\S+) -> (\S+)$")


def compute_stale(world: World, baseline: dict | None, existing: str = "") -> tuple[str, int]:
    """Render ledger/stale.md. Returns (text, open item count).

    An item is a (changed protected page -> page that links to it) pair. Items already ticked
    `[x]` in the existing file stay ticked for the same pair.
    """
    cleared = {(m.group(2), m.group(3)) for m in map(_STALE_LINE.match, existing.split("\n")) if m and m.group(1) == "x"}
    changes = classify_changes(world, baseline)
    reverse = world.reverse_links()
    items: list[tuple[str, str]] = []
    if baseline is not None:
        for file, kind in changes.items():
            if kind not in ("changed", "deleted"):
                continue
            was_protected = baseline["pages"].get(file, {}).get("protected", False)
            now_protected = file in world.pages and world.is_protected(world.pages[file])
            if not (was_protected or now_protected):
                continue
            for dependent in reverse.get(file, []):
                items.append((file, dependent))
            if kind == "deleted":
                for other, page in world.pages.items():
                    if file in page.page_links() and (file, other) not in items:
                        items.append((file, other))
    lines = [
        "# Stale dependents",
        "",
        "<!-- Generated by tools/canon_index.py; tick an item `[x]` once the dependent was checked (still fine / revised). -->",
        "",
    ]
    open_count = 0
    for changed, dependent in items:
        done = (changed, dependent) in cleared
        open_count += 0 if done else 1
        lines.append(f"- [{'x' if done else ' '}] {changed} -> {dependent}")
    if not items:
        lines.append("(none)")
    return "\n".join(lines) + "\n", open_count


def write_stale(world: World, baseline: dict | None) -> int:
    path = world.root / STALE_REL
    existing = read_text(path) if path.is_file() else ""
    text, open_count = compute_stale(world, baseline, existing)
    write_text(path, text)
    return open_count


def build_decisions_index(decisions: list[Record], root: Path | None = None) -> str:
    """decisions/INDEX.md: one row per decision so agents find the ones that affect their pages."""
    lines = [
        "# Decisions",
        "",
        "<!-- Generated by tools/canon_index.py decisions; do not edit. -->",
        "",
        "| Id | Type | Status | Blocking | Affects | Title |",
        "|---|---|---|---|---|---|",
    ]
    rows = []
    for rec in decisions:
        if rec.error:
            continue
        meta = rec.meta
        title = ""
        try:
            body = split_frontmatter(read_text((root or Path('.')) / rec.path))[1]
            title = next((line[2:].strip() for line in body.split("\n") if line.startswith("# ")), "")
        except (ValueError, OSError):
            pass
        rows.append((
            str(meta.get("id", "")), str(meta.get("type", "")), str(meta.get("status", "")),
            "yes" if meta.get("blocking") is True else "no",
            ", ".join(as_list(meta.get("affects"))) or "-", title or Path(rec.path).stem,
        ))
    for row in sorted(rows):
        lines.append("| " + " | ".join(c.replace("|", "/") for c in row) + " |")
    if not rows:
        lines.append("| (none) | | | | | |")
    return "\n".join(lines) + "\n"
