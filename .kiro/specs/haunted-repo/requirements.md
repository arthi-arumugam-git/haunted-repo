# Requirements: Haunted Repo

## Introduction
Haunted Repo inspects an abandoned Python repository and reports dead code ("zombies"), flaky tests ("poltergeists"), and stale or vulnerable dependencies ("cursed deps"), then writes a ranked Resurrection Plan.

## Requirement 1: Zombie detection
**User story:** As a maintainer inheriting a repo, I want unreferenced functions and classes listed, so that I can delete dead code safely.
1. WHEN the user runs a scan on a local path THE SYSTEM SHALL parse every `.py` file with the stdlib `ast` module.
2. THE SYSTEM SHALL report a top-level function or class as a zombie WHEN no other module or the same module references its name.
3. THE SYSTEM SHALL NOT report names listed in `__all__`, dunder names, or names referenced from tests.
4. IF a file fails to parse THEN THE SYSTEM SHALL record it as skipped with the error and continue.

## Requirement 2: Poltergeist detection
1. WHEN tests exist THE SYSTEM SHALL rerun the suite N times (default 5) in random order.
2. THE SYSTEM SHALL flag a test as a poltergeist WHEN its outcome differs across runs.

## Requirement 3: Cursed dependencies
1. THE SYSTEM SHALL query the public OSV API for each pinned dependency and list known vulnerabilities.

## Requirement 4: Resurrection Plan
1. THE SYSTEM SHALL write a markdown plan ranking findings by risk and effort.
2. WHERE the user opts in THE SYSTEM SHALL open one PR on the user's fork only; it SHALL NOT auto-merge.
