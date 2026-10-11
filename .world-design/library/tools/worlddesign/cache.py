"""A parse cache for the hooks: the parsed form of a page, keyed by the SHA-256 of its bytes.

Parsing every page is half of what the post-write hook spends. A page that has not changed parses to the same result, so the hook
keeps the result in `.world-design/cache/parse.json` and parses only the pages whose bytes changed.

The key is the content, not a timestamp, so there is no way for an entry to be stale: a page edited by Bash, by another provider or by
`git checkout` has different bytes and so a different key, and a tool that preserves the modification time changes nothing. The cache
is also dropped as a whole when the parser's source changes. Anything wrong with the file (missing, unreadable, corrupt, read-only
folder) means "no cache": the page is parsed as always. The lint that backstops the hooks (`canon_lint.py`, `finish_check.py`) does not
use it.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from . import world as worldmod
from .textio import normalize
from .world import Link, Page, parse_page

CACHE_REL = ".world-design/cache/parse.json"
FORMAT = 1


def parser_version() -> str:
    """Changes whenever the code that turns bytes into a Page changes."""
    source = Path(worldmod.__file__).read_bytes()
    return f"{FORMAT}:{hashlib.sha256(source).hexdigest()[:16]}"


class ParseCache:
    def __init__(self, root: Path | str):
        self.path = Path(root) / CACHE_REL
        self.version = parser_version()
        self.entries: dict[str, dict] = {}
        self.used: set[str] = set()
        self.dirty = False
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if data.get("version") == self.version and isinstance(data.get("pages"), dict):
                self.entries = data["pages"]
        except (OSError, ValueError, AttributeError):
            pass

    def parse(self, file: str, type_key: str, fields: dict, raw: bytes) -> Page:
        key = hashlib.sha256(raw).hexdigest()
        self.used.add(key)
        entry = self.entries.get(key)
        if entry is not None:
            try:
                return _rebuild(file, type_key, fields, raw, entry)
            except (KeyError, TypeError, ValueError):
                pass  # a damaged entry: parse again and replace it
        page = parse_page(file, type_key, fields, raw)
        self.entries[key] = _dump(page)
        self.dirty = True
        return page

    def save(self) -> None:
        """Write the cache if it changed (only the pages seen in this load are kept). Never raises."""
        stale = set(self.entries) - self.used
        if not self.dirty and not stale:
            return
        data = {"version": self.version, "pages": {k: v for k, v in self.entries.items() if k in self.used}}
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_name(f"{self.path.name}.{os.getpid()}.tmp")
            tmp.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
            os.replace(tmp, self.path)
        except OSError:
            pass


def _dump(page: Page) -> dict:
    kept = {number for number, _ in page.prose_lines}
    total = len(page.text.split("\n"))
    return {
        "name": page.name, "headings": [list(h) for h in page.headings], "links": [[l.label, l.target, l.line] for l in page.links],
        "facts": [list(f) for f in page.facts], "fenced": [n for n in range(1, total + 1) if n not in kept],
    }


def _rebuild(file: str, type_key: str, fields: dict, raw: bytes, entry: dict) -> Page:
    page = Page(file, type_key, fields, raw)
    page.text = normalize(raw.decode("utf-8", errors="replace").lstrip("﻿"))
    fenced = set(entry["fenced"])
    page.prose_lines = [(n, line) for n, line in enumerate(page.text.split("\n"), start=1) if n not in fenced]
    page.name = entry["name"]
    page.headings = [(int(h[0]), h[1], h[2], int(h[3])) for h in entry["headings"]]
    page.links = [Link(l[0], l[1], int(l[2])) for l in entry["links"]]
    page.facts = [(f[0], f[1], int(f[2])) for f in entry["facts"]]
    return page
