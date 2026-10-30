# Kiro Agent Hooks

This document describes the agent hooks planned for the Haunted Repo build. These hooks automate common workflows during development.

## Hook 1: On-Save Test Runner

**Trigger:** Save any file in `haunted/**/*.py`
**Action:** Run pytest for the corresponding test module
**Purpose:** Immediate feedback on code changes

```yaml
# Planned hook configuration
trigger: on_save
glob: "haunted/**/*.py"
command: pytest tests/test_$(basename $FILE .py).py -v
```

## Hook 2: On-Save Flake Detector

**Trigger:** Save any file in `tests/**/*.py`
**Action:** Run the changed test file 3 times with pytest-randomly
**Purpose:** Detect flaky tests introduced during development

```yaml
# Planned hook configuration
trigger: on_save
glob: "tests/**/*.py"
command: pytest $FILE --count=3 -p randomly -v
```

## Hook 3: Manual Resurrect

**Trigger:** Manual invocation
**Action:** Generate a Resurrection Plan for a configured demo victim repository
**Purpose:** Test the full analysis pipeline against a known target

```yaml
# Planned hook configuration
trigger: manual
name: "Resurrect"
command: python -m haunted.planner --repo $DEMO_VICTIM_URL --output resurrection-plan.md
```

## Implementation Status

These hooks are documented here as the planned automation for the build process. Implementation depends on Kiro IDE hook support and will be wired as the respective modules become functional.

## Demo Victims for Hook 3

Per DEMO_VICTIMS.md:
1. `mbianchidev/corn-test` - Flaky test demo (archived, read-only)
2. `box/flaky` - Zombie code + outdated deps demo
