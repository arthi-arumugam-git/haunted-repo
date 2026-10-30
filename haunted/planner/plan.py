"""Resurrection plan generation from analysis findings."""

from dataclasses import dataclass, field


@dataclass
class PlanItem:
    """A single item in the resurrection plan."""

    category: str  # "zombie", "poltergeist", "cursed"
    name: str
    description: str
    effort: str  # "low", "medium", "high"
    risk: str  # "low", "medium", "high"
    suggested_fix: str


@dataclass
class ResurrectionPlan:
    """Complete resurrection plan for a repository."""

    repo_url: str
    items: list[PlanItem] = field(default_factory=list)
    summary: str = ""

    def to_markdown(self) -> str:
        """Render the plan as markdown."""
        if not self.items:
            return f"# Resurrection Plan for {self.repo_url}\n\nNo issues found. This repo is not haunted."

        lines = [
            f"# Resurrection Plan for {self.repo_url}",
            "",
            self.summary,
            "",
            "## Issues",
            "",
        ]

        for item in self.items:
            lines.extend(
                [
                    f"### {item.category.title()}: {item.name}",
                    "",
                    f"**Description:** {item.description}",
                    f"**Effort:** {item.effort} | **Risk:** {item.risk}",
                    f"**Suggested fix:** {item.suggested_fix}",
                    "",
                ]
            )

        return "\n".join(lines)


def generate_plan(
    repo_url: str,
    analyzer_results: dict,
    flakes_results: dict,
    deps_results: dict,
) -> ResurrectionPlan:
    """
    Generate a resurrection plan from analysis results.

    Args:
        repo_url: URL of the analyzed repository
        analyzer_results: Output from haunted.analyzer
        flakes_results: Output from haunted.flakes
        deps_results: Output from haunted.deps

    Returns:
        ResurrectionPlan with ranked items
    """
    return ResurrectionPlan(
        repo_url=repo_url,
        items=[],
        summary="Analysis pending. Run full analysis to populate this plan.",
    )
