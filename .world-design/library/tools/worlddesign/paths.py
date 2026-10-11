"""Where the world is: one definition of "the nearest folder above here that has a manifest.json".

Light on purpose (no imports beyond the standard library's `os` and `pathlib`): the hooks import it on every tool call.
"""

from __future__ import annotations

import os
from pathlib import Path


def find_world_root(start: Path | str) -> Path | None:
    """`start` or the nearest folder above it that holds manifest.json, or None."""
    start = Path(start)
    for folder in (start, *start.parents):
        if (folder / "manifest.json").is_file():
            return folder
    return None


def hook_root(data: dict | None = None) -> Path | None:
    """The world a Claude Code hook belongs to: CLAUDE_PROJECT_DIR, else the workspace or cwd Claude Code sent, else the cwd."""
    data = data or {}
    start = os.environ.get("CLAUDE_PROJECT_DIR") or (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or Path.cwd()
    return find_world_root(Path(start))
