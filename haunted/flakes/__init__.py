"""Flakes module for detecting poltergeist (flaky) tests."""

from haunted.flakes.runner import detect_flaky_tests, FlakyTest

__all__ = ["detect_flaky_tests", "FlakyTest"]
