"""Poltergeist detection: rerun a pytest suite in shuffled orders (Req 2)."""
from __future__ import annotations

import random
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FlakeResult:
    runs: int
    outcomes: dict[str, list[str]] = field(default_factory=dict)

    @property
    def poltergeists(self) -> list[str]:
        return sorted(t for t, o in self.outcomes.items() if len(set(o)) > 1)


def collect(root: Path) -> list[str]:
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", f"--rootdir={root}"],
        cwd=root, capture_output=True, text=True,
    ).stdout
    return [l.strip() for l in out.splitlines() if "::" in l]


def _run_once(root: Path, order: list[str]) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as td:
        xml = Path(td) / "r.xml"
        subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", f"--rootdir={root}",
             f"--junitxml={xml}", *order],
            cwd=root, capture_output=True, text=True,
        )
        if not xml.exists():
            return {}
        res = {}
        for case in ET.parse(xml).iter("testcase"):
            cls, name = case.get("classname", ""), case.get("name", "")
            key = f"{cls}::{name}"
            status = "passed"
            for child in case:
                if child.tag in ("failure", "error"):
                    status = "failed"
                elif child.tag == "skipped":
                    status = "skipped"
            res[key] = status
        return res


def hunt(root: Path, runs: int = 5, seed: int | None = None) -> FlakeResult:
    """Rerun the suite `runs` times, each in a shuffled order; flag tests whose outcome changes."""
    root = Path(root).resolve()
    tests = collect(root)
    rng = random.Random(seed)
    result = FlakeResult(runs=runs)
    for _ in range(runs):
        order = tests[:]
        rng.shuffle(order)
        for t, status in _run_once(root, order).items():
            result.outcomes.setdefault(t, []).append(status)
    return result
