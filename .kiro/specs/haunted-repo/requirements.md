# Haunted Repo: Requirements Specification

## Overview
Haunted Repo analyzes abandoned Python repositories to find dead code, flaky tests, and outdated dependencies, then produces a ranked resurrection plan.

## Functional Requirements (EARS Format)

### R1: Repository Cloning
WHEN a user provides a public GitHub repository URL,
THE SYSTEM SHALL clone it read-only into a sandbox and build a module dependency graph.

### R2: Zombie Code Detection
THE SYSTEM SHALL identify "zombie" code: modules and functions with no inbound references and zero test coverage.

### R3: Poltergeist Test Detection
WHEN tests exist in the repository,
THE SYSTEM SHALL rerun the test suite N times (default: 5) and flag "poltergeist" tests whose pass/fail status changes across runs.

### R4: Cursed Dependency Audit
THE SYSTEM SHALL identify "cursed" dependencies defined as:
- End-of-life packages
- Packages with known CVEs
- Packages more than 2 major versions behind current

### R5: Resurrection Plan Generation
THE SYSTEM SHALL produce a ranked "Resurrection Plan" in markdown format containing:
- Each identified issue (zombie, poltergeist, or cursed dependency)
- Estimated effort to fix (low/medium/high)
- Risk level (low/medium/high)
- Suggested fix approach

### R6: Automated PR Creation (Opt-in)
WHERE the user opts in,
THE SYSTEM SHALL open a pull request that:
- Deletes confirmed zombie code
- Quarantines poltergeist tests with skip markers
- Updates cursed dependencies where safe
- Passes CI checks

## Non-Functional Requirements

### NF1: Read-Only by Default
THE SYSTEM SHALL NOT modify the original repository without explicit user consent.

### NF2: Public Repositories Only
THE SYSTEM SHALL only operate on public GitHub repositories.

### NF3: Python Focus
THE SYSTEM SHALL analyze Python codebases (Python 3.8+).

### NF4: No Paid APIs
THE SYSTEM SHALL use only free APIs (OSV, GitHub public API) for vulnerability and dependency data.
