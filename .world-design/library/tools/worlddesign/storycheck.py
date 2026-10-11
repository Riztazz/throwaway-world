"""Warnings for novels and series: the chapter ledger and the continuity ledger must stay in step with the prose.

K7 added `chapters.md` and `continuity.md` to a `form: novel` story and a `series.md` to a series. These checks make the
discipline mechanical: every chapter file has a ledger row, every drafted chapter has set at least one fact in the
continuity ledger, every chapter cited there exists, and a series lists the books that name it. Warnings only.
"""

from __future__ import annotations

import re
from pathlib import Path

from .issues import Issue
from .policy import Policy, load_policy
from .stories import SERIES_REL, load_stories, series_folders
from .textio import read_text


def _rows(text: str) -> list[tuple[list[str], list[str]]]:
    """(header cells, row cells) for every data row of every table in a markdown text."""
    out: list[tuple[list[str], list[str]]] = []
    header: list[str] = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            header = []
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?\s*$", lines[i + 1]):
            header = [c.lower() for c in cells]
        elif header and not re.match(r"^[\s:|-]+$", line.replace("|", "")):
            out.append((header, cells))
    return out


def _num(token: str) -> str:
    token = token.strip().lower().removeprefix("ch").removeprefix("chapter").strip()
    return str(int(token)) if token.isdigit() else token


def check_novel(folder: Path, rel: str, policy: Policy) -> list[Issue]:
    done_statuses = policy["lint.story_done_statuses"]
    issues: list[Issue] = []
    chapters = read_text(folder / "chapters.md") if (folder / "chapters.md").is_file() else ""
    continuity = read_text(folder / "continuity.md") if (folder / "continuity.md").is_file() else ""
    rows = [(h, c) for h, c in _rows(chapters) if "chapter" in h and "file" in h and len(c) == len(h)]
    ledger: dict[str, tuple[str, str]] = {}  # file -> (chapter id, status)
    for header, cells in rows:
        file = cells[header.index("file")]
        status = cells[header.index("status")].lower() if "status" in header else ""
        if file:
            ledger[file] = (_num(cells[header.index("chapter")]), status)
    prose = folder / "prose"
    files = sorted(f"prose/{p.name}" for p in prose.glob("*.md") if p.name.lower() != "readme.md") if prose.is_dir() else []
    for file in files:
        if file not in ledger:
            issues.append(Issue("warning", "L-STORY-CHAPTER", f"{rel}/chapters.md", f"{file} has no row in the chapter ledger"))
    for file in ledger:
        if file not in files:
            issues.append(Issue("warning", "L-STORY-CHAPTER", f"{rel}/chapters.md", f"the ledger lists {file}, which does not exist"))
    cited: set[str] = set()
    for header, cells in _rows(continuity):
        if "set in chapter" in header and len(cells) == len(header):
            cited |= {_num(t) for t in re.split(r"[,;/\s]+", cells[header.index("set in chapter")]) if t}
    known = {chapter for chapter, _ in ledger.values()}
    for file, (chapter, status) in sorted(ledger.items()):
        if status in done_statuses and chapter not in cited:
            issues.append(Issue("warning", "L-STORY-CONTINUITY", f"{rel}/continuity.md",
                                f"chapter {chapter} is {status} but no row in the continuity ledger says it was set in that chapter"))
    for chapter in sorted(cited - known - {""}):
        issues.append(Issue("warning", "L-STORY-CONTINUITY", f"{rel}/continuity.md", f"the continuity ledger cites chapter {chapter}, which is not in the chapter ledger"))
    return issues


def check_series(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    members: dict[str, list[str]] = {}
    for story in load_stories(root):
        if story.series:
            members.setdefault(story.series, []).append(story.rel)
    for folder in series_folders(root):
        rel = f"{SERIES_REL}/{folder.name}/series.md"
        text = read_text(folder / "series.md") if (folder / "series.md").is_file() else ""
        listed = []
        for header, cells in _rows(text):
            if "story folder" in header and len(cells) == len(header):
                listed.append(cells[header.index("story folder")].strip("`"))
        for path in listed:
            if path and "<" not in path and not (root / path).is_dir():
                issues.append(Issue("warning", "L-STORY-SERIES-BOOK", rel, f"the series lists {path}, which does not exist"))
        for path in members.get(folder.name, []):
            if path not in listed:
                issues.append(Issue("warning", "L-STORY-SERIES-BOOK", rel, f"{path} names this series but the Books table does not list it"))
    return issues


def check_novels(root: Path, policy: Policy | None = None) -> list[Issue]:
    policy = policy or load_policy(root)
    issues: list[Issue] = []
    for story in load_stories(root):
        if story.form == "novel":
            issues += check_novel(story.path, story.rel, policy)
    return issues + check_series(root)
