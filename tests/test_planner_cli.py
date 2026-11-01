from pathlib import Path

from haunted.__main__ import main
from haunted.analyzer import ScanResult, scan
from haunted.planner import render_plan

FIXTURE = Path(__file__).parent / "fixtures" / "victim"


def test_plan_ranks_parse_errors_before_zombies():
    plan = render_plan("victim", scan(FIXTURE))
    assert plan.index("broken.py") < plan.index("forgotten")
    assert "OldThing" in plan


def test_empty_plan():
    assert "resting peacefully" in render_plan("x", ScanResult())


def test_cli_writes_file(tmp_path):
    out = tmp_path / "plan.md"
    assert main(["scan", str(FIXTURE), "-o", str(out)]) == 0
    assert "Resurrection plan" in out.read_text()


def test_cli_rejects_missing_dir(tmp_path):
    assert main(["scan", str(tmp_path / "nope")]) == 2
