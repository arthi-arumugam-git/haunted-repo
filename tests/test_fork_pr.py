import io
import json
import shlex
from pathlib import Path

import pytest

from haunted import fork_pr
from haunted.__main__ import main
from haunted.fork_pr import BRANCH, PLAN_FILE, ForkPRError, open_fork_pr, plan_summary

FIXTURE = Path(__file__).parent / "fixtures" / "victim"

PLAN = """# Resurrection plan for `victim`

## Fix first: files that do not parse

1. `broken.py`: invalid syntax. Risk high, effort low.

## Then: unreferenced code to review or delete

2. `core.py:3` function `forgotten` has no references. Risk low, effort low.
3. `core.py:9` class `OldThing` has no references. Risk low, effort low.
"""


class FakeRunner:
    def __init__(self, user="ghost", owner="ghost"):
        self.user, self.owner = user, owner
        self.calls: list[list[str]] = []

    def __call__(self, cmd, cwd):
        self.calls.append(cmd)
        if cmd[:3] == ["git", "remote", "get-url"]:
            return f"https://github.com/{self.owner}/victim.git\n"
        if cmd[:3] == ["gh", "api", "user"]:
            return self.user + "\n"
        if cmd[:3] == ["gh", "repo", "view"]:
            return json.dumps({"owner": {"login": self.owner}, "name": "victim", "defaultBranchRef": {"name": "main"}})
        if cmd[:3] == ["gh", "pr", "create"]:
            return f"https://github.com/{self.owner}/victim/pull/1\n"
        return ""


def _mutating(calls):
    return [c for c in calls if c[:2] in (["git", "checkout"], ["git", "add"], ["git", "commit"], ["git", "push"])
            or c[:3] == ["gh", "pr", "create"]]


def test_dry_run_prints_commands_and_runs_nothing(tmp_path):
    runner, out = FakeRunner(), io.StringIO()
    assert open_fork_pr(tmp_path, PLAN, runner=runner, dry_run=True, out=out) is None
    text = out.getvalue()
    assert f"git checkout -b {BRANCH}" in text
    assert f"git commit -m 'Add resurrection plan from haunted-repo' -- {PLAN_FILE}" in text
    assert f"git push -u origin {BRANCH}" in text
    assert f"gh pr create --repo ghost/victim --base main --head {BRANCH}" in text
    assert _mutating(runner.calls) == []
    assert not (tmp_path / PLAN_FILE).exists()


def test_refuses_when_owner_is_not_gh_user(tmp_path):
    runner = FakeRunner(user="ghost", owner="upstream-org")
    with pytest.raises(ForkPRError, match="upstream-org"):
        open_fork_pr(tmp_path, PLAN, runner=runner, dry_run=False, out=io.StringIO())
    assert _mutating(runner.calls) == []
    assert not (tmp_path / PLAN_FILE).exists()


def test_real_run_commits_plan_opens_pr_and_never_merges(tmp_path):
    runner, out = FakeRunner(), io.StringIO()
    url = open_fork_pr(tmp_path, PLAN, runner=runner, dry_run=False, out=out)
    assert url == "https://github.com/ghost/victim/pull/1"
    assert (tmp_path / PLAN_FILE).read_text() == PLAN
    assert [c[:3] for c in _mutating(runner.calls)] == [
        ["git", "checkout", "-b"], ["git", "add", PLAN_FILE], ["git", "commit", "-m"],
        ["git", "push", "-u"], ["gh", "pr", "create"],
    ]
    for cmd in runner.calls:
        assert "merge" not in cmd and "--auto" not in cmd


def test_pr_body_contains_plan_summary(tmp_path):
    runner = FakeRunner()
    open_fork_pr(tmp_path, PLAN, runner=runner, dry_run=False, out=io.StringIO())
    create = next(c for c in runner.calls if c[:3] == ["gh", "pr", "create"])
    body = create[create.index("--body") + 1]
    assert "- Fix first: files that do not parse: 1" in body
    assert "- Then: unreferenced code to review or delete: 2" in body
    assert "will not be merged automatically" in body


def test_summary_of_empty_plan():
    assert plan_summary("# Resurrection plan for `x`\n\nNo findings.\n") == "No findings. This repo is resting peacefully."


def test_cli_open_pr_without_yes_is_dry_run(tmp_path, monkeypatch, capsys):
    runner = FakeRunner()
    monkeypatch.setattr(fork_pr, "run", runner)
    assert main(["scan", str(FIXTURE), "--no-osv", "-o", str(tmp_path / "plan.md"), "--open-pr"]) == 0
    err = capsys.readouterr().err
    assert "Dry run." in err and shlex.join(["git", "push", "-u", "origin", BRANCH]) in err
    assert _mutating(runner.calls) == []


def test_cli_refusal_exits_nonzero(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(fork_pr, "run", FakeRunner(owner="someone-else"))
    assert main(["scan", str(FIXTURE), "--no-osv", "-o", str(tmp_path / "plan.md"), "--open-pr", "--yes"]) == 1
    assert "refusing" in capsys.readouterr().err
