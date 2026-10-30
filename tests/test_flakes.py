"""Tests for the flakes module."""

from pathlib import Path

from haunted.flakes import detect_flaky_tests, FlakyTest


def test_detect_flaky_tests_returns_dict():
    """detect_flaky_tests returns a dictionary with expected keys."""
    result = detect_flaky_tests(Path("/tmp/nonexistent"))

    assert isinstance(result, dict)
    assert "flaky_tests" in result
    assert "total_tests" in result
    assert "runs_completed" in result


def test_detect_flaky_tests_custom_runs():
    """detect_flaky_tests accepts custom run count."""
    result = detect_flaky_tests(Path("/tmp/nonexistent"), runs=10)

    assert result["status"] == "stub"


def test_flaky_test_dataclass():
    """FlakyTest dataclass can be instantiated."""
    flaky = FlakyTest(
        name="test_random_behavior",
        module="test_utils.py",
        pass_count=3,
        fail_count=2,
        total_runs=5,
        error_messages=["AssertionError: 4 != 5"],
    )

    assert flaky.name == "test_random_behavior"
    assert flaky.pass_count == 3
    assert flaky.fail_count == 2
    assert flaky.total_runs == 5
