"""CLI: python -m haunted scan <path> [-o plan.md]"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from haunted.analyzer import scan
from haunted.planner import render_plan


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="haunted")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("scan", help="scan a Python repo and print a resurrection plan")
    sp.add_argument("path")
    sp.add_argument("-o", "--output", help="write the plan to this file")
    args = ap.parse_args(argv)
    root = Path(args.path)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    plan = render_plan(root.name, scan(root))
    if args.output:
        Path(args.output).write_text(plan, encoding="utf-8")
    else:
        sys.stdout.write(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
