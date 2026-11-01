"""CLI: python -m haunted scan <path> [-o plan.md] [--flaky-runs N] [--no-osv]"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from haunted.analyzer import scan
from haunted.flake import hunt
from haunted.osv import audit
from haunted.planner import render_plan


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="haunted")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("scan", help="scan a Python repo and print a resurrection plan")
    sp.add_argument("path")
    sp.add_argument("-o", "--output", help="write the plan to this file")
    sp.add_argument("--flaky-runs", type=int, default=0, help="rerun the test suite N times in shuffled order (0 = skip)")
    sp.add_argument("--no-osv", action="store_true", help="skip the OSV vulnerability lookup for pinned deps")
    args = ap.parse_args(argv)
    root = Path(args.path)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    flakes = hunt(root, runs=args.flaky_runs).poltergeists if args.flaky_runs > 0 else []
    cursed = []
    if not args.no_osv:
        try:
            cursed = audit(root)
        except (OSError, ValueError) as e:
            print(f"OSV lookup failed, skipping dependency audit: {e}", file=sys.stderr)
    plan = render_plan(root.name, scan(root), flakes, cursed)
    if args.output:
        Path(args.output).write_text(plan, encoding="utf-8")
    else:
        sys.stdout.write(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
