"""A tiny frontmatter reader for decision and ledger files (never used for world/ pages).

Supports exactly what our templates use: `key: value` lines, inline lists `[a, b]`, quoted
or bare strings, true/false, and trailing `# comments`. Anything else raises ValueError so
a malformed record is reported instead of silently misread.
"""

from __future__ import annotations

import re
from typing import Any

_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s+(.*))?$")


def _strip_comment(value: str) -> str:
    out, quote = [], ""
    for i, ch in enumerate(value):
        if quote:
            out.append(ch)
            if ch == quote and value[i - 1] != "\\":
                quote = ""
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#" and (i == 0 or value[i - 1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out).strip()


def _scalar(token: str) -> Any:
    token = token.strip()
    if token in ("", "null", "~"):
        return "" if token == "" else None
    if token == "true":
        return True
    if token == "false":
        return False
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        inner = token[1:-1]
        return inner.replace('\\"', '"').replace("\\\\", "\\") if token[0] == '"' else inner
    return token


def _split_list(inner: str) -> list[str]:
    items, current, quote = [], [], ""
    for ch in inner:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            current.append(ch)
        elif ch == ",":
            items.append("".join(current))
            current = []
        else:
            current.append(ch)
    tail = "".join(current)
    if tail.strip() or items:
        items.append(tail)
    return [i for i in items if i.strip()]


def parse_value(raw: str) -> Any:
    value = _strip_comment(raw)
    if value.startswith("["):
        if not value.endswith("]"):
            raise ValueError(f"Unterminated list: {raw!r}")
        return [_scalar(i) for i in _split_list(value[1:-1])]
    return _scalar(value)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (metadata, body). Raises ValueError when frontmatter is missing or malformed."""
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        end = text.find("\n---", 4)
        if end < 0 or text[end + 4 :].strip():
            raise ValueError("unterminated frontmatter")
        block, body = text[4:end], ""
    else:
        block, body = text[4:end], text[end + 5 :]
    meta: dict[str, Any] = {}
    for number, line in enumerate(block.split("\n"), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = _KEY.match(line)
        if not match:
            raise ValueError(f"line {number}: unsupported frontmatter syntax: {line!r}")
        key, raw = match.group(1), match.group(2) or ""
        if key in meta:
            raise ValueError(f"line {number}: repeated key {key}")
        meta[key] = parse_value(raw)
    return meta, body
