"""Cursed dependencies: look up pinned deps in the public OSV database (Req 3)."""
from __future__ import annotations

import json
import re
import tomllib
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

OSV_API = "https://api.osv.dev/v1"

# name[extras]==version, with no other specifiers after it
_PIN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*==\s*([A-Za-z0-9][A-Za-z0-9._+!-]*)$")

Http = Callable[[str, "dict | None"], dict]


@dataclass(frozen=True)
class Dep:
    name: str
    version: str
    source: str


@dataclass(frozen=True)
class Vuln:
    id: str
    summary: str
    aliases: tuple[str, ...] = ()


@dataclass
class CursedDep:
    dep: Dep
    vulns: list[Vuln] = field(default_factory=list)


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_pin(spec: str) -> tuple[str, str] | None:
    spec = spec.split(";", 1)[0].split(" #", 1)[0].strip()
    m = _PIN.match(spec)
    return (_normalize(m.group(1)), m.group(2)) if m else None


def find_deps(root: Path) -> list[Dep]:
    root = Path(root)
    deps: dict[tuple[str, str], Dep] = {}

    def add(spec: str, source: str) -> None:
        pin = parse_pin(spec)
        if pin and pin not in deps:
            deps[pin] = Dep(pin[0], pin[1], source)

    for req in sorted(root.glob("requirements*.txt")):
        for line in req.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith(("#", "-")):
                add(line, req.name)
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        try:
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            data = {}
        for spec in data.get("project", {}).get("dependencies", []):
            add(spec, pyproject.name)
    return list(deps.values())


def urllib_http(url: str, body: dict | None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # nosec B310
        return json.load(resp)


def audit(root: Path, http: Http = urllib_http) -> list[CursedDep]:
    """Return pinned deps with known OSV vulnerabilities. Network errors propagate."""
    deps = find_deps(root)
    if not deps:
        return []
    queries = [{"package": {"name": d.name, "ecosystem": "PyPI"}, "version": d.version} for d in deps]
    results = http(f"{OSV_API}/querybatch", {"queries": queries}).get("results", [])
    details: dict[str, Vuln] = {}
    cursed = []
    for dep, res in zip(deps, results):
        ids = [v["id"] for v in res.get("vulns", [])]
        if not ids:
            continue
        for vid in ids:
            if vid not in details:
                v = http(f"{OSV_API}/vulns/{vid}", None)
                details[vid] = Vuln(vid, v.get("summary", ""), tuple(v.get("aliases", [])))
        kept: list[Vuln] = []
        for v in (details[i] for i in ids):
            if not any(v.id in k.aliases for k in kept):
                kept.append(v)
        cursed.append(CursedDep(dep, kept))
    return cursed
