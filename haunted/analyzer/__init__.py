"""Find unreferenced top-level functions and classes (zombies) in a Python tree."""
from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist"}


@dataclass(frozen=True)
class Zombie:
    path: str
    name: str
    kind: str
    lineno: int


@dataclass
class ScanResult:
    zombies: list[Zombie] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)


def _iter_py(root: Path):
    for p in sorted(root.rglob("*.py")):
        if not SKIP_DIRS.intersection(p.relative_to(root).parts):
            yield p


def _exported(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
        ) and isinstance(node.value, (ast.List, ast.Tuple)):
            names |= {e.value for e in node.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)}
    return names


def _dotted_tail(expr: ast.expr) -> str | None:
    if isinstance(expr, ast.Call):
        expr = expr.func
    if isinstance(expr, ast.Attribute):
        return expr.attr
    if isinstance(expr, ast.Name):
        return expr.id
    return None


def _runner_invoked(node: ast.stmt) -> bool:
    if isinstance(node, ast.ClassDef):
        return node.name.startswith("Test") or any(
            (_dotted_tail(b) or "").endswith("TestCase") for b in node.bases
        )
    return node.name.startswith(("test", "pytest_")) or any(
        _dotted_tail(d) == "fixture" for d in node.decorator_list
    )


def scan(root: str | Path) -> ScanResult:
    root = Path(root)
    result = ScanResult()
    defs: list[Zombie] = []
    refs: set[str] = set()
    exported: set[str] = set()
    for path in _iter_py(root):
        rel = str(path.relative_to(root))
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=rel)
        except SyntaxError as exc:
            result.skipped[rel] = f"SyntaxError: {exc.msg} (line {exc.lineno})"
            continue
        exported |= _exported(tree)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not _runner_invoked(node):
                kind = "class" if isinstance(node, ast.ClassDef) else "function"
                defs.append(Zombie(rel, node.name, kind, node.lineno))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                refs.add(node.id)
            elif isinstance(node, ast.Attribute):
                refs.add(node.attr)
            elif isinstance(node, ast.alias):
                refs.add(node.name.split(".")[-1])
                if node.asname:
                    refs.add(node.asname)
    for d in defs:
        if d.name.startswith("__") or d.name in exported or d.name in refs:
            continue
        result.zombies.append(d)
    return result
