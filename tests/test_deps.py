"""Tests for the deps module."""

from pathlib import Path

from haunted.deps import audit_dependencies, CursedDependency


def test_audit_dependencies_returns_dict():
    """audit_dependencies returns a dictionary with expected keys."""
    result = audit_dependencies(Path("/tmp/nonexistent"))

    assert isinstance(result, dict)
    assert "cursed_deps" in result
    assert "total_deps" in result
    assert "cve_count" in result
    assert "outdated_count" in result


def test_cursed_dependency_dataclass():
    """CursedDependency dataclass can be instantiated."""
    cursed = CursedDependency(
        name="requests",
        installed_version="2.20.0",
        latest_version="2.31.0",
        curse_type="cve",
        severity="high",
        details="CVE-2023-32681: Unintended leak of Proxy-Authorization header",
    )

    assert cursed.name == "requests"
    assert cursed.curse_type == "cve"
    assert cursed.severity == "high"


def test_cursed_dependency_outdated():
    """CursedDependency can represent outdated packages."""
    cursed = CursedDependency(
        name="django",
        installed_version="2.2.0",
        latest_version="5.0.0",
        curse_type="outdated",
        severity="medium",
        details="3 major versions behind current",
    )

    assert cursed.curse_type == "outdated"
