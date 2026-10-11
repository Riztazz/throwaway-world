"""Load a world (manifest.json + world/), parse pages, and build the index.

Used by both tools/canon_index.py and tools/canon_lint.py so they always agree about a
page's name, links and fact lines.

Layout (see docs/WORLD-HANDOFF.md):
    <world-root>/manifest.json
    <world-root>/world/*.md            flat; no subfolders
    <world-root>/ledger/, decisions/    outside world/
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .textio import normalize
from typing import TYPE_CHECKING

from .types import PAGE_FILE_RE, TypeTable, load_types

if TYPE_CHECKING:
    from .cache import ParseCache

_FENCE = re.compile(r"^\s{0,3}(```+|~~~+)")
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)")
_FACT = re.compile(r"^::([a-z][a-z0-9-]*)::\s*(.*?)\s*$")
_CODE_SPAN = re.compile(r"`[^`]*`")
_EXTERNAL = re.compile(r"^(https?://|mailto:|/|#)")


def heading_slug(text: str) -> str:
    """GitHub-style anchor: lowercase, drop punctuation, spaces become dashes."""
    text = re.sub(r"[*_`]", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9 \-]", "", text)
    return text.replace(" ", "-")


@dataclass(frozen=True)
class Link:
    label: str
    target: str  # raw target
    line: int


@dataclass
class Page:
    file: str
    type_key: str
    fields: dict
    raw: bytes
    text: str = ""
    name: str = ""
    headings: list[tuple[int, str, str, int]] = field(default_factory=list)  # level, text, slug, line
    links: list[Link] = field(default_factory=list)
    facts: list[tuple[str, str, int]] = field(default_factory=list)  # key, value, line
    prose_lines: list[tuple[int, str]] = field(default_factory=list)  # (line no, text) outside code fences

    @property
    def slug(self) -> str:
        return self.file[:-3]

    @property
    def status(self) -> str:
        return str(self.fields.get("status", ""))

    @property
    def summary(self) -> str:
        return str(self.fields.get("summary", ""))

    def sha256(self) -> str:
        return hashlib.sha256(normalize(self.raw.decode("utf-8", errors="replace")).encode("utf-8")).hexdigest()

    def fact_map(self) -> dict[str, str]:
        return {k: v for k, v, _ in self.facts}

    def page_links(self) -> list[str]:
        """Page file names this page links to (relative `.md` targets only)."""
        out = []
        for link in self.links:
            if _EXTERNAL.match(link.target):
                continue
            path = link.target.split("#", 1)[0]
            if path.endswith(".md") and path not in out:
                out.append(path)
        return out


def parse_page(file: str, type_key: str, fields: dict, raw: bytes) -> Page:
    page = Page(file, type_key, fields, raw)
    page.text = normalize(raw.decode("utf-8", errors="replace").lstrip("﻿"))
    in_fence = ""
    for number, line in enumerate(page.text.split("\n"), start=1):
        fence = _FENCE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = marker
            elif in_fence == marker:
                in_fence = ""
            continue
        if in_fence:
            continue
        page.prose_lines.append((number, line))
        heading = _HEADING.match(line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            page.headings.append((level, text, heading_slug(text), number))
            if level == 1 and not page.name:
                page.name = text
        fact = _FACT.match(line)
        if fact:
            page.facts.append((fact.group(1), fact.group(2), number))
        for match in _LINK.finditer(_CODE_SPAN.sub("", line)):
            page.links.append(Link(match.group(1), match.group(2).strip(), number))
    return page


@dataclass
class World:
    root: Path
    manifest: dict
    pages: dict[str, Page]  # by file name, manifest order
    types: TypeTable
    problems: list[str] = field(default_factory=list)  # structural problems found while loading

    @property
    def world_dir(self) -> Path:
        return self.root / "world"

    def reverse_links(self) -> dict[str, list[str]]:
        reverse: dict[str, list[str]] = {f: [] for f in self.pages}
        for page in self.pages.values():
            for target in page.page_links():
                if target in reverse and page.file not in reverse[target]:
                    reverse[target].append(page.file)
        return reverse

    def is_protected(self, page: Page) -> bool:
        return page.status == "accepted" or page.type_key in self.types.core_rule_keys()


def load_world(root: Path | str, types: TypeTable | None = None, cache: "ParseCache | None" = None) -> World:
    """Load manifest and pages. `cache` (worlddesign/cache.py) skips re-parsing pages whose bytes are unchanged; the hooks pass one."""
    root = Path(root)
    types = types or load_types()
    manifest_path = root / "manifest.json"
    problems: list[str] = []
    if not manifest_path.is_file():
        raise FileNotFoundError(f"No manifest.json in {root}")
    try:
        manifest = json.loads(manifest_path.read_bytes().decode("utf-8-sig"))  # a BOM is a lint error (H-BOM), never a reason to stop loading
    except (ValueError, UnicodeDecodeError) as error:
        raise ValueError(f"manifest.json is not valid UTF-8 JSON: {error}") from None
    world = World(root, manifest, {}, types, problems)
    rows = manifest.get("pages")
    if not isinstance(rows, list):
        problems.append("manifest.json needs a `pages` array")
        rows = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("file"), str):
            problems.append(f"manifest page row needs a `file`: {row!r}")
            continue
        file = row["file"]
        if file in world.pages:
            problems.append(f"manifest lists {file} more than once")
            continue
        path = world.world_dir / file
        raw = path.read_bytes() if path.is_file() else b""
        parse = cache.parse if cache is not None else parse_page
        world.pages[file] = parse(file, str(row.get("typeKey", "")), dict(row.get("fields") or {}), raw)
        if not path.is_file():
            problems.append(f"manifest names {file} but it is not in world/")
    return world


def build_index(world: World) -> str:
    """INDEX.md: one row per page. Agents read this first, then open only relevant pages."""
    reverse = world.reverse_links()
    lines = [
        "# Index",
        "",
        "<!-- Generated by tools/canon_index.py; do not edit. -->",
        "",
        f"{len(world.pages)} pages. Query links with `py -3 tools/canon_index.py links-to <page>` and facts with `facts --key <key>`.",
        "",
        "| Page | Name | Type | Status | Summary | Links to | Linked from |",
        "|---|---|---|---|---|---|---|",
    ]
    for file, page in world.pages.items():
        def cell(items: list[str]) -> str:
            return ", ".join(i[:-3] for i in items) or "-"
        summary = page.summary.replace("|", "/").replace("\n", " ") or "-"
        lines.append(
            f"| {page.slug} | {page.name or '-'} | {page.type_key} | {page.status or '-'} | {summary} "
            f"| {cell(page.page_links())} | {cell(reverse.get(file, []))} |"
        )
    return "\n".join(lines) + "\n"


def page_hash_snapshot(world: World, created: str) -> dict:
    """The baseline written by `canon_index.py snapshot`; only run at a user-approved checkpoint."""
    pages = {}
    for file, page in world.pages.items():
        pages[file] = {
            "sha256": page.sha256(),
            "type": page.type_key,
            "status": page.status,
            "protected": world.is_protected(page),
            "facts": page.fact_map(),
        }
    return {"version": 1, "created": created, "pages": pages}


def is_valid_page_file(name: str) -> bool:
    return bool(PAGE_FILE_RE.match(name))
