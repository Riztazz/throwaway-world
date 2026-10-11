"""A single reported problem, shared by the lint and the SVG checker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Issue:
    level: str  # "error" | "warning"
    code: str  # stable id, e.g. "H-LINK-TARGET"
    where: str  # file (and line) the problem is in
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.code:18} {self.where}: {self.message}"


def errors(issues: list[Issue]) -> list[Issue]:
    return [i for i in issues if i.level == "error"]
