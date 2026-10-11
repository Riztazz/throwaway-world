"""The STUDIO page types (from docs/WORLD-HANDOFF.md) as data, plus page and manifest templates."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .textio import read_text

SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
PAGE_FILE_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*\.md$")
_DEFAULT_PATH = Path(__file__).resolve().parents[2] / "templates" / "world" / "types.json"


@dataclass(frozen=True)
class PageType:
    key: str
    order: int | None
    holds: str
    lead_skill: str | None
    core_rule: bool
    sections: tuple[str, ...]
    fields: tuple[str, ...]
    refs: tuple[str, ...]


@dataclass(frozen=True)
class TypeTable:
    status_values: tuple[str, ...]
    types: dict[str, PageType]

    def get(self, key: str) -> PageType:
        try:
            return self.types[key]
        except KeyError:
            raise KeyError(f"Unknown page type key: {key}") from None

    def core_rule_keys(self) -> frozenset[str]:
        return frozenset(k for k, t in self.types.items() if t.core_rule)


def load_types(path: Path | str | None = None) -> TypeTable:
    data = json.loads(read_text(path or _DEFAULT_PATH))
    types: dict[str, PageType] = {}
    for item in data["types"]:
        key = item["key"]
        if key in types or not SLUG_RE.match(key):
            raise ValueError(f"Invalid or repeated type key: {key}")
        unknown_refs = set(item["refs"]) - set(item["fields"])
        if unknown_refs:
            raise ValueError(f"Type {key}: refs not in fields: {sorted(unknown_refs)}")
        types[key] = PageType(
            key, item["order"], item["holds"], item["lead_skill"], bool(item["core_rule"]),
            tuple(item["sections"]), tuple(item["fields"]), tuple(item["refs"]),
        )
    return TypeTable(tuple(data["status_values"]), types)


def page_template(page_type: PageType, name: str) -> str:
    """A new page body: `# Name`, then the type's sections as `##` headings. No frontmatter."""
    lines = [f"# {name}", ""]
    for section in page_type.sections:
        lines += [f"## {section}", "", ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def manifest_row(page_type: PageType, file: str, summary: str = "", status: str = "draft") -> dict:
    """A manifest `pages` row with every field the type allows, empty until filled."""
    if not PAGE_FILE_RE.match(file):
        raise ValueError(f"Page file name must be a slug ending in .md: {file}")
    fields: dict[str, str] = {"status": status, "summary": summary}
    for name in page_type.fields:
        fields[name] = ""
    return {"file": file, "typeKey": page_type.key, "fields": fields}
