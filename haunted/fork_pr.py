"""Open one resurrection-plan PR on the user's own fork (Req 4.2). Never merges."""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

BRANCH = "haunted/resurrection-plan"
PLAN_FILE = "RESURRECTION_PLAN.md"
TITLE = "Add resurrection plan from haunted-repo"

Runner = Callable[[list[str], Path], str]


class ForkPRError(Exception):
    pass


def run(cmd: list[str], cwd: Path) -> str:
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True).stdout  # nosec B603
    except FileNotFoundError as e:
        raise ForkPRError(f"{cmd[0]} not found on PATH") from e
    except subprocess.CalledProcessError as e:
        raise ForkPRError(f"{shlex.join(cmd)} failed: {e.stderr.strip()}") from e


def plan_summary(plan: str) -> str:
    """One bullet per plan section with its item count, e.g. '- Fix first: files that do not parse: 2'."""
    counts: dict[str, int] = {}
    section = None
    for line in plan.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            counts[section] = 0
        elif section and re.match(r"\d+\. ", line):
            counts[section] += 1
    if not counts:
        return "No findings. This repo is resting peacefully."
    return "\n".join(f"- {name}: {n}" for name, n in counts.items())


def pr_body(plan: str) -> str:
    return "\n".join([
        f"Findings from `haunted scan`. The full ranked plan is in `{PLAN_FILE}`.",
        "",
        plan_summary(plan),
        "",
        "This PR was opened by haunted-repo and will not be merged automatically. Review it and merge or close it yourself.",
        "",
    ])


def fork_target(root: Path, runner: Runner) -> tuple[str, str]:
    """Return (owner/name, default branch) for the origin remote, refusing unless the gh user owns it."""
    origin = runner(["git", "remote", "get-url", "origin"], root).strip()
    user = runner(["gh", "api", "user", "--jq", ".login"], root).strip()
    info = json.loads(runner(["gh", "repo", "view", origin, "--json", "owner,name,defaultBranchRef"], root))
    owner = info["owner"]["login"]
    if owner.lower() != user.lower():
        raise ForkPRError(
            f"refusing to open a PR: origin is owned by {owner!r}, but gh is logged in as {user!r}. "
            "haunted only opens PRs on your own fork."
        )
    return f"{owner}/{info['name']}", info["defaultBranchRef"]["name"]


def pr_commands(slug: str, base: str, plan: str) -> list[list[str]]:
    return [
        ["git", "checkout", "-b", BRANCH],
        ["git", "add", PLAN_FILE],
        ["git", "commit", "-m", TITLE, "--", PLAN_FILE],
        ["git", "push", "-u", "origin", BRANCH],
        ["gh", "pr", "create", "--repo", slug, "--base", base, "--head", BRANCH, "--title", TITLE,
         "--body", pr_body(plan)],
    ]


def open_fork_pr(root: Path, plan: str, runner: Runner | None = None, dry_run: bool = True,
                 out: TextIO | None = None) -> str | None:
    """Commit the plan on BRANCH and open a PR against the user's fork. In dry run, print the commands instead.

    Returns the PR URL printed by gh, or None for a dry run.
    """
    runner = runner or run
    out = out or sys.stderr
    root = Path(root).resolve()
    slug, base = fork_target(root, runner)
    cmds = pr_commands(slug, base, plan)
    if dry_run:
        print(f"Dry run. Would write {PLAN_FILE} in {root} and run:", file=out)
        for cmd in cmds:
            print("  " + shlex.join(cmd), file=out)
        print("Rerun with --open-pr --yes to do it.", file=out)
        return None
    (root / PLAN_FILE).write_text(plan, encoding="utf-8")
    url = ""
    for cmd in cmds:
        url = runner(cmd, root).strip()
    print(f"Opened {url}", file=out)
    return url
