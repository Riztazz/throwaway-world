"""Stories and series on disk: one reader for `drafts/stories/<slug>/` that the lint, the novel and series checks, the session summary
and the entry facts all use, so they cannot disagree about what a story is.

A story folder is any folder under `drafts/stories/` whose name does not start with `_` (those are templates). `story.md` carries the
frontmatter (`status`, `form`, `series`, `book`). Reading never raises: a missing or broken `story.md` is reported on the record, and
each caller decides what that means (the lint calls it an error, the summary calls the story a draft).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .miniyaml import split_frontmatter
from .textio import read_text

STORIES_REL = "drafts/stories"
SERIES_REL = "drafts/series"
STORY_FORMS = ("short", "novella", "novel")
NOVEL_FILES = ("chapters.md", "continuity.md")
STORY_ROW_STATUSES = ("open", "replaced", "promoted", "demoted")
NEW_TAG = re.compile(r'\{\{new:\s*([a-z][a-z-]*)\s*,\s*"([^"]+)"\s*\}\}')


@dataclass
class Story:
    slug: str
    path: Path
    has_story_md: bool = False
    meta: dict = field(default_factory=dict)
    error: str = ""  # why story.md could not be read, "" when it could (or is missing)

    @property
    def rel(self) -> str:
        return f"{STORIES_REL}/{self.slug}"

    @property
    def status(self) -> str:
        """The status as written; "draft" when story.md is missing or unreadable (a lint error is raised for those separately)."""
        return str(self.meta.get("status", "")) if self.has_story_md and not self.error else "draft"

    @property
    def is_final(self) -> bool:
        return self.status == "final"

    @property
    def form(self) -> str:
        return str(self.meta.get("form", ""))

    @property
    def series(self) -> str:
        return str(self.meta.get("series") or "").strip()


def story_folders(root: Path | str) -> list[Path]:
    base = Path(root) / STORIES_REL
    return sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("_")) if base.is_dir() else []


def series_folders(root: Path | str) -> list[Path]:
    base = Path(root) / SERIES_REL
    return sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("_")) if base.is_dir() else []


def load_stories(root: Path | str) -> list[Story]:
    stories = []
    for folder in story_folders(root):
        story = Story(folder.name, folder, has_story_md=(folder / "story.md").is_file())
        if story.has_story_md:
            try:
                story.meta, _ = split_frontmatter(read_text(folder / "story.md"))
            except (OSError, ValueError) as error:
                story.error = str(error)
        stories.append(story)
    return stories


def invention_rows(path: Path) -> tuple[dict[tuple[str, str], tuple[str, str]], list[str]]:
    """Rows of a story's inventions.md as {(name lower, type): (status, resolution)}, plus format problems."""
    rows: dict[tuple[str, str], tuple[str, str]] = {}
    problems: list[str] = []
    if not path.is_file():
        return rows, ["inventions.md is missing"]
    for raw in read_text(path).split("\n"):
        line = raw.strip()
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0].lower() == "item":
            continue
        if len(cells) != 5:
            problems.append(f"row needs 5 columns (Item, Type, Where, Status, Resolution): {line[:60]}")
            continue
        name, kind, _where, status, resolution = cells
        if status not in STORY_ROW_STATUSES:
            problems.append(f"row `{name}` has status `{status}`; use {', '.join(STORY_ROW_STATUSES)}")
            continue
        rows[(name.lower(), kind.lower())] = (status, resolution)
    return rows, problems


def open_invention_count(folder: Path) -> int:
    """Rows still open in a story's inventions.md (a missing file or a malformed row counts as none)."""
    rows, _ = invention_rows(folder / "inventions.md")
    return sum(1 for status, _ in rows.values() if status == "open")
