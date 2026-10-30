"""Tests for the planner module."""

from haunted.planner import generate_plan, ResurrectionPlan
from haunted.planner.plan import PlanItem


def test_generate_plan_returns_resurrection_plan():
    """generate_plan returns a ResurrectionPlan instance."""
    result = generate_plan(
        repo_url="https://github.com/example/repo",
        analyzer_results={"zombie_modules": [], "zombie_functions": []},
        flakes_results={"flaky_tests": []},
        deps_results={"cursed_deps": []},
    )

    assert isinstance(result, ResurrectionPlan)
    assert result.repo_url == "https://github.com/example/repo"


def test_resurrection_plan_to_markdown_empty():
    """ResurrectionPlan renders markdown for empty results."""
    plan = ResurrectionPlan(
        repo_url="https://github.com/example/repo",
        items=[],
    )

    md = plan.to_markdown()

    assert "https://github.com/example/repo" in md
    assert "No issues found" in md


def test_resurrection_plan_to_markdown_with_items():
    """ResurrectionPlan renders markdown with items."""
    plan = ResurrectionPlan(
        repo_url="https://github.com/example/repo",
        items=[
            PlanItem(
                category="zombie",
                name="old_utils.py",
                description="Module has no inbound references",
                effort="low",
                risk="low",
                suggested_fix="Delete the module after confirming no runtime imports",
            ),
        ],
        summary="Found 1 issue in this repository.",
    )

    md = plan.to_markdown()

    assert "old_utils.py" in md
    assert "zombie" in md.lower()
    assert "low" in md.lower()


def test_plan_item_dataclass():
    """PlanItem dataclass can be instantiated."""
    item = PlanItem(
        category="poltergeist",
        name="test_flaky",
        description="Test flips between pass and fail",
        effort="medium",
        risk="low",
        suggested_fix="Add pytest.mark.flaky or fix the root cause",
    )

    assert item.category == "poltergeist"
    assert item.effort == "medium"
