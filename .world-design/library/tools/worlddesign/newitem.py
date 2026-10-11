"""Scaffold a story, a series or a game system spec from the world's own templates, with the frontmatter filled in.

Replaces copying template folders by hand. It never overwrites anything.
"""

from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

from .textio import read_text, write_text

SLUG = re.compile(r"^[a-z][a-z0-9-]{1,40}$")
FORMS = ("short", "novella", "novel")


class NewItemError(ValueError):
    pass


def _slug(value: str) -> str:
    if not SLUG.match(value):
        raise NewItemError("the slug is lowercase letters, digits and dashes, starting with a letter (2 to 41 characters)")
    return value


def _title(slug: str) -> str:
    return slug.replace("-", " ").title()


def _copy(src: Path, dst: Path, skip: tuple[str, ...] = ()) -> None:
    for path in sorted(src.rglob("*")):
        if path.is_file() and path.name not in skip:
            target = dst / path.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)


def _need(path: Path, what: str) -> Path:
    if not path.exists():
        raise NewItemError(f"this world has no {what} ({path.name} is missing); it was probably created without it")
    return path


def new_story(root: Path, slug: str, form: str = "short", series: str = "", book: str = "", today: str | None = None) -> list[str]:
    slug = _slug(slug)
    if form not in FORMS:
        raise NewItemError(f"form must be one of {', '.join(FORMS)}")
    if series:
        _slug(series)
        if not (root / "drafts" / "series" / series / "series.md").is_file():
            raise NewItemError(f"series `{series}` does not exist: create it first with `new_item.py series {series}`")
        if not book.isdigit():
            raise NewItemError("a book in a series needs --book N")
    dest = root / "drafts" / "stories" / slug
    if dest.exists():
        raise NewItemError(f"drafts/stories/{slug} already exists; nothing was changed")
    template = _need(root / "drafts" / "stories" / "_template", "story template")
    _copy(template, dest)
    if form == "novel":
        _copy(_need(root / "drafts" / "stories" / "_template-novel", "novel template"), dest, skip=("README.md",))
    story = dest / "story.md"
    text = read_text(story)
    text = re.sub(r"(?m)^id:.*$", f"id: {slug}", text, count=1)
    text = re.sub(r"(?m)^title:.*$", f"title: {_title(slug)}", text, count=1)
    text = re.sub(r"(?m)^form:.*$", f"form: {form}", text, count=1)
    text = re.sub(r"(?m)^created:.*$", f"created: {today or date.today().isoformat()}", text, count=1)
    text = re.sub(r"(?m)^# series:.*$", f"series: {series}" if series else "# series: series-slug", text, count=1)
    text = re.sub(r"(?m)^# book:.*$", f"book: {book}" if series else "# book: 1", text, count=1)
    text = re.sub(r"(?m)^# Working title$", f"# {_title(slug)}", text, count=1)
    write_text(story, text)
    made = [f"drafts/stories/{slug}/"]
    notes = ["fill in story.md (premise, viewpoint contract) before drafting; every `{{new: ...}}` tag needs a row in inventions.md"]
    if form == "novel":
        notes.append("keep chapters.md and continuity.md up to date at the end of every chapter")
    if series:
        notes.append(f"add the book to the Books table in drafts/series/{series}/series.md")
    return made + notes


def new_series(root: Path, slug: str, today: str | None = None) -> list[str]:
    slug = _slug(slug)
    dest = root / "drafts" / "series" / slug
    if dest.exists():
        raise NewItemError(f"drafts/series/{slug} already exists; nothing was changed")
    _copy(_need(root / "drafts" / "series" / "_template", "series template"), dest)
    path = dest / "series.md"
    text = read_text(path)
    text = re.sub(r"(?m)^id:.*$", f"id: {slug}", text, count=1)
    text = re.sub(r"(?m)^title:.*$", f"title: {_title(slug)}", text, count=1)
    text = re.sub(r"(?m)^created:.*$", f"created: {today or date.today().isoformat()}", text, count=1)
    text = re.sub(r"(?m)^# Working title of the series$", f"# {_title(slug)}", text, count=1)
    write_text(path, text)
    return [f"drafts/series/{slug}/", f"create each book with `new_item.py story BOOK-SLUG --form novel --series {slug} --book N`, and list it in the Books table"]


def new_system(root: Path, slug: str) -> list[str]:
    slug = _slug(slug)
    template = _need(root / "design" / "systems" / "_template.md", "systems template (only game worlds have one)")
    dest = root / "design" / "systems" / f"{slug}.md"
    if dest.exists():
        raise NewItemError(f"design/systems/{slug}.md already exists; nothing was changed")
    write_text(dest, re.sub(r"(?m)^# System name$", f"# {_title(slug)}", read_text(template), count=1))
    return [f"design/systems/{slug}.md", "prose only: no balance numbers (the lint warns); name the tuning parameters without values"]
