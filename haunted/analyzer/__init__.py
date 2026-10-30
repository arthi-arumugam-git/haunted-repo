"""Analyzer module for detecting zombie (dead) code."""

from haunted.analyzer.graph import analyze_repository, ZombieModule, ZombieFunction

__all__ = ["analyze_repository", "ZombieModule", "ZombieFunction"]
