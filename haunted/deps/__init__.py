"""Deps module for auditing cursed (outdated/vulnerable) dependencies."""

from haunted.deps.audit import audit_dependencies, CursedDependency

__all__ = ["audit_dependencies", "CursedDependency"]
