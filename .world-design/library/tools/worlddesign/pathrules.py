"""Claude Code path-scoped rules, generated from `rules/`.

A file in `.claude/rules/` with `paths:` frontmatter is loaded when Claude reads or edits a matching file (checked live:
the page rule appears after reading a world page and not after reading a design file). That puts the right rule text next to
the work again, including after compaction, in long sessions that the single-turn evals do not exercise. The text is copied,
never hand-written, so it cannot drift from `rules/`; `@import` is not relied on. Claude Code only.
"""

from __future__ import annotations

from pathlib import Path

from .textio import read_text

# (output file, source file under rules/ or None, paths it applies to)
RULES = (
    ("world-pages.md", "PAGES.md", ("world/**", "manifest.json")),
    ("world-stories.md", "STORIES.md", ("drafts/stories/**", "drafts/series/**")),
    ("world-ledger.md", "INVENTION.md", ("ledger/**",)),
    ("world-decisions.md", "DECISIONS.md", ("decisions/**",)),
    ("world-references.md", None, ("authoring/references/**",)),
)

REFERENCE_RULES = """# Reference cards and research

Cards describe transferable techniques in your own words. Quote at most a few words from a source, never passages, and do not summarize plot. For every card record the source and its type (the work itself, an excerpt the user supplied, or secondary commentary), how it was read (raw text, a fetched summary, the user's words), the edition or episode, the locator, what you did **not** read, your confidence, the spoiler ceiling, and whether the reference is `hard` or `soft`. Never cite a chapter, page or timecode that came only from secondary commentary or from memory; mark anything you could not access `not read`. Samples are original and in this world's language, never excerpts. A hard reference may not be dropped silently; a soft one may be set aside with a one-line reason. The lint (`L-CARD-*`, `L-REF-*`) checks the shape.

"""


def _frontmatter(paths: tuple[str, ...]) -> str:
    return "---\npaths:\n" + "".join(f'  - "{p}"\n' for p in paths) + "---\n"


def path_rules(repo: Path) -> dict[str, str]:
    """{`.claude/rules/<name>`: text} generated from the library's rules, for a world."""
    out: dict[str, str] = {}
    for name, source, paths in RULES:
        card = repo / "templates" / "world" / "authoring" / "references" / "CARD-TEMPLATE.md"
        needed = repo / "rules" / source if source else card
        if not needed.is_file():  # a trimmed library snapshot may lack a source: leave that rule out rather than fail
            continue
        body = read_text(needed).rstrip("\n") + "\n" if source else REFERENCE_RULES + read_text(card).rstrip("\n") + "\n"
        origin = f"rules/{source}" if source else "the reference rules and CARD-TEMPLATE.md"
        out[f".claude/rules/{name}"] = (_frontmatter(paths) + f"\n<!-- Generated from {origin} by the bootstrapper; do not edit. Loaded when a matching file is read or edited. -->\n\n" + body)
    return out
