"""Deterministic text I/O: UTF-8, no BOM on write, LF line endings.

Reading normalizes CRLF/CR to LF so generated output and hashes do not depend on a
checkout's line-ending settings (the old Node generator embedded CRLF from role briefs,
which made adapters differ between machines).
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path


def normalize(text: str) -> str:
    """Return text with CRLF and lone CR converted to LF."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text(path: Path | str) -> str:
    """Read UTF-8 text (a leading BOM is dropped) with LF endings."""
    data = Path(path).read_bytes()
    return normalize(data.decode("utf-8-sig"))


def write_text(path: Path | str, text: str) -> None:
    """Write UTF-8 without BOM, converting any CRLF to LF, creating parent folders."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(normalize(text).encode("utf-8"))


def js_trim(text: str) -> str:
    """Trim like JavaScript's String.prototype.trim (whitespace plus U+FEFF)."""
    return text.strip().strip("﻿").strip()


def use_utf8() -> None:
    """Make stdin, stdout and stderr UTF-8 whatever the console code page is.

    On Windows a pipe is encoded with the locale (cp1252 or cp1250), so a Polish name raises `UnicodeEncodeError` or
    reaches Claude Code as mojibake. Every entry point calls this first. A stream that cannot be reconfigured (a test's
    in-memory buffer) is left alone.
    """
    for stream, errors in ((sys.stdin, "replace"), (sys.stdout, "replace"), (sys.stderr, "replace")):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors=errors)
            except (OSError, ValueError):
                pass


def fold(text: str) -> str:
    """Lowercase and strip accents, so `Wiedźmin` is `wiedzmin` and `Łódź` is `lodz`."""
    text = text.replace("ł", "l").replace("Ł", "L")
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c))


def slug(text: str) -> str:
    """`Jarosław Grzędowicz` -> `jaroslaw-grzedowicz`: folded, then letters and digits joined by single dashes."""
    return re.sub(r"[^a-z0-9]+", "-", fold(text)).strip("-")
