"""Keyword search over a world: pages, fact lines, decisions and the invention log.

For "does this already exist?" before inventing (the duplicate-entity failure): exact, deterministic, accent- and
case-insensitive, no index to keep fresh. Every word of the query must appear in the item; items are ranked by where the
query matches (name, fact key, summary, fact value, decision, log line, body).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .ledger import as_list, load_decisions
from .textio import fold, read_text
from .world import World


@dataclass(frozen=True)
class Hit:
    score: int
    where: str   # file or file:line
    kind: str    # name | fact | summary | decision | log | body
    snippet: str

    def __str__(self) -> str:
        return f"{self.score:>3}  {self.where}  [{self.kind}]  {self.snippet}"


def _words(query: str) -> list[str]:
    return [w for w in re.findall(r"\w+", fold(query))]


def _has(text: str, words: list[str]) -> bool:
    folded = fold(text)
    return all(w in folded for w in words)


def _clip(text: str, width: int = 110) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1] + "…"


def search(world: World, query: str, type_key: str = "", status: str = "", limit: int = 20) -> list[Hit]:
    words = _words(query)
    if not words:
        return []
    phrase = " ".join(words)
    hits: list[Hit] = []
    for file, page in sorted(world.pages.items()):
        if type_key and page.type_key != type_key:
            continue
        if status and page.status != status:
            continue
        best: Hit | None = None

        def offer(score: int, where: str, kind: str, snippet: str) -> None:
            nonlocal best
            if best is None or score > best.score:
                best = Hit(score, where, kind, _clip(snippet))
        if _has(page.name, words):
            offer(100 + (20 if phrase in fold(page.name) else 0), f"world/{file}", "name", page.name)
        if _has(file[:-3].replace("-", " "), words):
            offer(90, f"world/{file}", "name", file)
        for key, value, line in page.facts:
            if _has(key.replace("-", " "), words):
                offer(60, f"world/{file}:{line}", "fact", f"::{key}:: {value}")
            elif _has(value, words):
                offer(30, f"world/{file}:{line}", "fact", f"::{key}:: {value}")
        if page.summary and _has(page.summary, words):
            offer(40, f"world/{file}", "summary", page.summary)
        if best is None:
            for number, line in page.prose_lines:
                if _has(line, words):
                    offer(10, f"world/{file}:{number}", "body", line)
                    break
        if best is not None:
            hits.append(best)
    if not type_key and not status:
        for rec in load_decisions(world.root):
            if rec.error:
                continue
            text = read_text(world.root / rec.path)
            title = next((l[2:].strip() for l in text.split("\n") if l.startswith("# ")), rec.path)
            if _has(text, words):
                hits.append(Hit(20 + (10 if _has(title, words) else 0), rec.path, "decision",
                                f"{rec.meta.get('id')} ({rec.meta.get('status')}): {title}; affects {', '.join(as_list(rec.meta.get('affects'))) or '-'}"))
        log = world.root / "ledger" / "log.md"
        if log.is_file():
            for number, line in enumerate(read_text(log).split("\n"), start=1):
                if re.match(r"^\d{4}-\d{2}-\d{2} \|", line) and _has(line, words):
                    hits.append(Hit(15, f"ledger/log.md:{number}", "log", line))
    hits.sort(key=lambda h: (-h.score, h.where))
    return hits[:limit]
