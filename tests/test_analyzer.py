"""Tests for the analyzer module."""

from pathlib import Path

from haunted.analyzer import analyze_repository, ZombieModule, ZombieFunction


def test_analyze_repository_returns_dict():
    """analyze_repository returns a dictionary with expected keys."""
    result = analyze_repository(Path("/tmp/nonexistent"))

    assert isinstance(result, dict)
    assert "zombie_modules" in result
    assert "zombie_functions" in result
    assert "module_count" in result
    assert "function_count" in result


def test_zombie_module_dataclass():
    """ZombieModule dataclass can be instantiated."""
    zombie = ZombieModule(
        path="src/old.py",
        name="old",
        line_count=50,
        reason="No references found",
    )

    assert zombie.path == "src/old.py"
    assert zombie.name == "old"
    assert zombie.line_count == 50


def test_zombie_function_dataclass():
    """ZombieFunction dataclass can be instantiated."""
    zombie = ZombieFunction(
        module="utils.py",
        name="deprecated_helper",
        line_number=42,
        reason="No callers",
    )

    assert zombie.module == "utils.py"
    assert zombie.name == "deprecated_helper"
    assert zombie.line_number == 42
