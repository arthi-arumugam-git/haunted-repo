"""Dependency auditing for CVEs, EOL packages, and outdated versions."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CursedDependency:
    """A dependency with security or freshness issues."""

    name: str
    installed_version: str
    latest_version: str | None
    curse_type: str  # "cve", "eol", "outdated"
    severity: str  # "low", "medium", "high", "critical"
    details: str


def audit_dependencies(repo_path: Path) -> dict:
    """
    Audit repository dependencies for security and freshness issues.

    Args:
        repo_path: Path to the cloned repository

    Returns:
        Dictionary containing:
        - cursed_deps: List of CursedDependency
        - total_deps: Total dependencies found
        - cve_count: Dependencies with known CVEs
        - outdated_count: Dependencies more than 2 majors behind
    """
    return {
        "cursed_deps": [],
        "total_deps": 0,
        "cve_count": 0,
        "outdated_count": 0,
        "status": "stub",
    }
