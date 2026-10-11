"""Policy: the numbers, lists and levels the tools use, kept apart from the code that runs them.

The mechanism (a check, a hook, a guard) stays small; what it is tuned to lives in `policy_defaults.json` next to this
file, and a world may override single keys in `.agents/narrative/policy.json`, the same way `models.json` overrides the
model map. Unknown keys and wrong types are refused loudly, so a typo never silently changes nothing.

    policy = load_policy(root)           # defaults, or defaults plus the world's override
    policy["lint.card_sample_max_words"]  # a dotted key; a missing key raises
    policy.check_level("L-FACT-ORDER")   # "off", "warning" or "error" for the finding code (see worlddesign/checks.py)

`checks` maps a finding code (see worlddesign/codes.py) to `off`, `warning` or `error`. Only a code whose default level is
a warning can be tuned: an error protects canon or the import contract and stays an error, and the handoff checks (`H-*`)
are the STUDIO import contract, warnings included.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .codes import CODES
from .textio import read_text

DEFAULTS_PATH = Path(__file__).resolve().parent / "policy_defaults.json"
OVERRIDE_REL = ".agents/narrative/policy.json"
LEVELS = ("off", "warning", "error")
LOCKED_PREFIXES = ("H-",)  # the STUDIO import contract: not a matter of taste, whatever its level


class PolicyError(ValueError):
    pass


@lru_cache(maxsize=1)
def _defaults() -> dict:
    return json.loads(DEFAULTS_PATH.read_text(encoding="utf-8"))


def _flatten(tree: dict, prefix: str = "") -> dict[str, object]:
    flat: dict[str, object] = {}
    for key, value in tree.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict) and name != "checks":
            flat.update(_flatten(value, name + "."))
        else:
            flat[name] = value
    return flat


def default_keys() -> list[str]:
    return sorted(_flatten(_defaults()))


class Policy:
    def __init__(self, values: dict[str, object], checks: dict[str, str]):
        self._values = values
        self._checks = checks

    def __getitem__(self, key: str):
        try:
            return self._values[key]
        except KeyError:
            raise KeyError(f"unknown policy key {key!r}") from None

    def check_level(self, code: str, default: str) -> str:
        """The level the finding `code` is reported at: the policy's choice, else the check's own default."""
        return self._checks.get(code, default)


def _validate(values: dict[str, object], override: dict) -> tuple[dict[str, object], dict[str, str]]:
    merged = dict(values)
    checks: dict[str, str] = {}
    for key, value in _flatten(override).items():
        if key == "checks":
            if not isinstance(value, dict):
                raise PolicyError("checks must be an object mapping a finding code to off, warning or error")
            for code, level in value.items():
                if level not in LEVELS:
                    raise PolicyError(f"checks.{code}: {level!r} is not one of {', '.join(LEVELS)}")
                if code not in CODES:
                    raise PolicyError(f"checks.{code}: no such finding code (see worlddesign/codes.py)")
                if str(code).startswith(LOCKED_PREFIXES):
                    raise PolicyError(f"checks.{code}: handoff checks (H-*) are the STUDIO import contract and cannot be changed")
                if CODES[code] != "warning":
                    raise PolicyError(f"checks.{code}: an error protects canon or the import contract; only warnings can be tuned")
                checks[str(code)] = level
            continue
        if key not in values:
            raise PolicyError(f"unknown policy key {key!r} (known: {', '.join(sorted(values))})")
        base = values[key]
        if type(value) is not type(base):
            raise PolicyError(f"{key}: expected {type(base).__name__}, got {type(value).__name__}")
        if isinstance(base, list) and (not value or any(not isinstance(v, str) or not v.strip() for v in value)):
            raise PolicyError(f"{key}: a non-empty list of non-empty strings is required")
        if isinstance(base, int) and value < 1:
            raise PolicyError(f"{key}: must be at least 1")
        merged[key] = value
    return merged, checks


def load_policy(root: Path | str | None = None) -> Policy:
    """The defaults, plus the world's `.agents/narrative/policy.json` when `root` has one."""
    values = _flatten(_defaults())
    values.pop("checks", None)
    path = Path(root) / OVERRIDE_REL if root is not None else None
    if path is None or not path.is_file():
        return Policy(values, {})
    try:
        override = json.loads(read_text(path))
    except ValueError as error:
        raise PolicyError(f"{OVERRIDE_REL} is not valid JSON: {error}") from None
    if not isinstance(override, dict):
        raise PolicyError(f"{OVERRIDE_REL} must be a JSON object")
    merged, checks = _validate(values, override)
    return Policy(merged, checks)
