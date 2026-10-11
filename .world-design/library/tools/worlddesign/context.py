"""Read-only context preparation and freshness checks for project-bound narrative roles.

Port of the retired Node loader (kept in evals/baselines/library-v0/scripts) with one addition: the reference fallback chain
(plan decision 24). It never writes files and never launches an agent.

A packet holds, in order: the project manifest, the library registry, the shared contract, the role
brief, the role's base skills, the project skills and context the manifest binds to the role, and
then the role's reference chain: authoring/references/roles/<role>.md, authoring/references/
categories/<id>.md for each category that lists the role, and voice.md. Missing reference levels
are reported in `references`, not treated as errors, unless `strict` is set.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .cli import Parser
from .render import parse_registry
from .textio import normalize

MANIFEST = ".agents/narrative/project.json"
CATEGORIES = "agents/reference-categories.json"
MAX_FILE_BYTES = 128 * 1024
MAX_CONTEXT_BYTES = 256 * 1024
MAX_PACKET_BYTES = 2 * 1024 * 1024
MAX_INPUTS = 64

_PART = re.compile(r"^[a-zA-Z0-9_.-]+$")
_SKILL_PATH = re.compile(r"^\.agents/narrative/skills/[a-z][a-z0-9-]{0,63}/SKILL\.md$")
_PROJECT_ID = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
_PACKET_KEYS = {"version", "projectId", "revision", "role", "inputs", "references"}
_INPUT_KEYS = {"source", "kind", "path", "sha256", "text"}


class ContextError(ValueError):
    """A context problem the coordinator must report instead of working around."""


def portable_path(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) <= 240
        and not value.startswith("/")
        and all(_PART.match(p) and p not in (".", "..") and not p.endswith(".") for p in value.split("/"))
    )


def _paths(value: Any, skill: bool) -> list[str]:
    if not isinstance(value, list) or len(value) > 32:
        raise ContextError("Required paths must be an array of at most 32 entries")
    result: list[str] = []
    for item in value:
        if not portable_path(item) or (skill and not _SKILL_PATH.match(item)) or (not skill and not item.endswith(".md")) or item in result:
            raise ContextError(f"Invalid or duplicate required path: {item}")
        result.append(item)
    return result


def parse_project_manifest(value: Any, known_roles: set[str]) -> dict:
    """Validate all bindings syntactically; only the selected role's files are loaded."""
    if (
        not isinstance(value, dict)
        or set(value) != {"version", "projectId", "revision", "roles"}
        or value["version"] != 1
        or not isinstance(value["projectId"], str)
        or not _PROJECT_ID.match(value["projectId"])
        or not isinstance(value["revision"], str)
        or not value["revision"].strip()
        or len(value["revision"]) > 80
        or not isinstance(value["roles"], dict)
    ):
        raise ContextError("Project manifest needs version 1, projectId, revision and roles")
    roles: dict[str, dict] = {}
    for role_id, binding in value["roles"].items():
        if role_id not in known_roles:
            raise ContextError(f"Unknown narrative role in project manifest: {role_id}")
        if not isinstance(binding, dict) or set(binding) != {"requiredSkills", "requiredContext"}:
            raise ContextError(f"Role binding needs requiredSkills and requiredContext: {role_id}")
        skills = _paths(binding["requiredSkills"], True)
        context = _paths(binding["requiredContext"], False)
        if set(skills) & set(context):
            raise ContextError(f"A file cannot be both a project skill and reference context: {role_id}")
        roles[role_id] = {"requiredSkills": skills, "requiredContext": context}
    return {"version": 1, "projectId": value["projectId"], "revision": value["revision"], "roles": roles}


def _read_text(path: Path, limit: int) -> str:
    if not path.is_file():
        raise ContextError(f"Input must be a regular file within size limit: {path}")
    if path.stat().st_size > limit:
        raise ContextError(f"Input exceeds size limit: {path}")
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ContextError(f"Input must contain nonempty UTF-8 text: {path}") from None
    if not text.strip() or "\0" in text:
        raise ContextError(f"Input must contain nonempty UTF-8 text: {path}")
    return normalize(text.lstrip("﻿"))


def load_input(root: Path, source: str, kind: str, rel: str) -> dict:
    if not portable_path(rel):
        raise ContextError(f"Unsafe context path: {rel}")
    real_root = root.resolve(strict=True)
    target = (real_root / rel).resolve(strict=True)
    if not target.is_relative_to(real_root):
        raise ContextError(f"Context path escapes its root: {rel}")
    text = _read_text(target, MAX_FILE_BYTES)
    return {"source": source, "kind": kind, "path": rel, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "text": text}


def _category_ids_for(library: Path, role_id: str) -> tuple[list[str], set[str]]:
    data = json.loads(_read_text(library / CATEGORIES, MAX_FILE_BYTES))
    ids = [c["id"] for c in data["categories"] if role_id in c["roles"]]
    return ids, set(data.get("required_roles", ()))


def prepare_project_context(library_root: Path | str, project_root: Path | str, role_id: str, strict: bool = False) -> dict:
    library, project = Path(library_root), Path(project_root)
    registry = load_input(library, "library", "registry", "agents/registry.json")
    profiles = parse_registry(json.loads(registry["text"]))
    role = next((p for p in profiles if p.id == role_id), None)
    if role is None:
        raise ContextError(f"Unknown narrative role: {role_id}")
    manifest_input = load_input(project, "project", "manifest", MANIFEST)
    manifest = parse_project_manifest(json.loads(manifest_input["text"]), {p.id for p in profiles})
    binding = manifest["roles"].get(role_id)
    if binding is None:
        raise ContextError(f"Configure a project binding for role: {role_id}")

    inputs = [
        manifest_input,
        registry,
        load_input(library, "library", "contract", "agents/contract.md"),
        load_input(library, "library", "role", f"agents/{role.path}"),
        *[load_input(library, "library", "base-skill", f"skills/{s}/SKILL.md") for s in role.skills],
        *[load_input(project, "project", "project-skill", p) for p in binding["requiredSkills"]],
        *[load_input(project, "project", "context", p) for p in binding["requiredContext"]],
    ]

    category_ids, required = _category_ids_for(library, role_id)
    wanted = [("role", f"authoring/references/roles/{role_id}.md")]
    wanted += [("category", f"authoring/references/categories/{c}.md") for c in category_ids]
    wanted += [("voice", "voice.md")]
    status: dict[str, Any] = {"role": None, "categories": [], "voice": False, "missing": [], "configured": False,
                              "required": role_id in required}
    for level, rel in wanted:
        if (project / rel).is_file():
            inputs.append(load_input(project, "project", "reference", rel))
            if level == "role":
                status["role"] = rel
            elif level == "category":
                status["categories"].append(rel)
            else:
                status["voice"] = True
        else:
            status["missing"].append(rel)
    status["configured"] = status["voice"] and (status["role"] is not None or bool(status["categories"]))
    if strict and status["required"] and not status["configured"]:
        raise ContextError(f"Role {role_id} needs references but has none configured; missing: {', '.join(status['missing'])}")

    if len(inputs) > MAX_INPUTS or sum(len(i["text"].encode("utf-8")) for i in inputs) > MAX_CONTEXT_BYTES:
        raise ContextError("Required context exceeds the 64-file / 256 KiB packet budget; narrow the binding")
    return {"version": 1, "projectId": manifest["projectId"], "revision": manifest["revision"], "role": role_id,
            "inputs": inputs, "references": status}


def verify_project_context(library_root: Path | str, project_root: Path | str, packet: Any) -> dict:
    """Detect missing, changed or tampered inputs; this does not evaluate creative compliance."""
    if (
        not isinstance(packet, dict)
        or set(packet) != _PACKET_KEYS
        or packet["version"] != 1
        or not isinstance(packet["projectId"], str)
        or not isinstance(packet["revision"], str)
        or not isinstance(packet["role"], str)
        or not isinstance(packet["inputs"], list)
        or len(packet["inputs"]) > MAX_INPUTS
    ):
        raise ContextError("Invalid project context packet")
    current = prepare_project_context(library_root, project_root, packet["role"])
    if (packet["projectId"] != current["projectId"] or packet["revision"] != current["revision"]
            or len(packet["inputs"]) != len(current["inputs"]) or packet["references"] != current["references"]):
        raise ContextError("Project context is stale or incomplete; prepare it again")
    for index, now in enumerate(current["inputs"]):
        old = packet["inputs"][index]
        if not isinstance(old, dict) or set(old) != _INPUT_KEYS or any(old[k] != now[k] for k in _INPUT_KEYS):
            raise ContextError(f"Project context changed or was altered at input {index}; prepare it again")
    return current


class _ContextParser(Parser):
    def error(self, message: str):  # a usage error is a ContextError, like every other problem here
        raise ContextError(f"{message} (see --help)")


def _context_parser() -> argparse.ArgumentParser:
    parser = _ContextParser(prog="context.py", description="Prepare the context packet for one narrative role in a world project, or verify a saved packet is "
                            "still current. The project manifest stays at .agents/narrative/project.json.")
    sub = parser.add_subparsers(dest="mode", required=True, metavar="prepare|verify", parser_class=_ContextParser)
    prepare = sub.add_parser("prepare", help="write the context packet for a role to stdout")
    prepare.add_argument("--project", required=True, help="the world folder")
    prepare.add_argument("--role", required=True, help="a role id")
    prepare.add_argument("--library", help="the library (default: this one)")
    prepare.add_argument("--strict", action="store_true", help="fail unless the role has its reference card")
    verify = sub.add_parser("verify", help="check that a saved packet is still current")
    verify.add_argument("--project", required=True, help="the world folder")
    verify.add_argument("--packet", required=True, help="the saved packet")
    verify.add_argument("--library", help="the library (default: this one)")
    return parser


def run_project_context(args: list[str], cwd: Path, default_library: Path) -> str:
    parser = _context_parser()
    if args in (["--help"], ["-h"]):
        return parser.format_help().rstrip("\n")
    opts = parser.parse_args(args)
    library = (cwd / opts.library).resolve() if opts.library else default_library
    project = (cwd / opts.project).resolve()
    if opts.mode == "prepare":
        return json.dumps(prepare_project_context(library, project, opts.role, opts.strict), indent=2, ensure_ascii=False)
    packet_path = (cwd / opts.packet).resolve()
    packet = json.loads(_read_text(packet_path, MAX_PACKET_BYTES))
    verified = verify_project_context(library, project, packet)
    return f"project context: {verified['projectId']} / {verified['role']} / {len(verified['inputs'])} inputs unchanged"
