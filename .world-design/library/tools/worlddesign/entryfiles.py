"""Render the world's coordinator entry files from their templates.

`AGENTS.md` is the real file (Codex reads it; the facts block in it is refreshed by `canon_index.py entry`). `CLAUDE.md` imports it
with `@AGENTS.md` and adds only what exists in Claude Code (hooks, `/world-mode`, output style, rules). The import is the documented
way to share one file between the two providers, and was verified live on Claude Code 2.1.296: Claude read both files. Codex does not
read CLAUDE.md. Both are generated, not edited by hand, and AGENTS.md stays well under Codex's 32 KiB limit.
"""

from __future__ import annotations

from pathlib import Path

from .textio import read_text

TEMPLATES = Path(__file__).resolve().parents[2] / "templates" / "world"
TEMPLATE = TEMPLATES / "AGENTS.md.tmpl"
CLAUDE_TEMPLATE = TEMPLATES / "CLAUDE.md.tmpl"
CODEX_LIMIT_BYTES = 32 * 1024


def render_entry_files(project_name: str, template: Path | str | None = None) -> dict[str, str]:
    name = project_name.strip()
    if not name or "\n" in name:
        raise ValueError("project name must be a single non-empty line")
    body = read_text(template or TEMPLATE).replace("{{PROJECT_NAME}}", name)
    claude = read_text(CLAUDE_TEMPLATE).replace("{{PROJECT_NAME}}", name)
    if "{{" in body or "{{" in claude:
        raise ValueError("unreplaced placeholder in the entry-file template")
    if len(body.encode("utf-8")) > CODEX_LIMIT_BYTES:
        raise ValueError("entry file exceeds the 32 KiB Codex AGENTS.md limit")
    return {"AGENTS.md": body, "CLAUDE.md": claude}
