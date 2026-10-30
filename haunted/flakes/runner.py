"""Pytest runner for flaky test detection."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FlakyTest:
    """A test that produces inconsistent results across runs."""

    name: str
    module: str
    pass_count: int
    fail_count: int
    total_runs: int
    error_messages: list[str]


def detect_flaky_tests(repo_path: Path, runs: int = 5) -> dict:
    """
    Run tests multiple times to detect flaky behavior.

    Args:
        repo_path: Path to the cloned repository
        runs: Number of times to run the test suite

    Returns:
        Dictionary containing:
        - flaky_tests: List of FlakyTest
        - total_tests: Total tests discovered
        - runs_completed: Number of runs finished
    """
    return {
        "flaky_tests": [],
        "total_tests": 0,
        "runs_completed": 0,
        "status": "stub",
    }
