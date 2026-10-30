# Product Steering

## Target User
Maintainers who inherit or adopt an abandoned Python repository and need to assess its health before investing effort.

## Job to Be Done
Find dead code, flaky tests, and stale dependencies in a Python repo, then propose a ranked fix plan and one safe cleanup PR.

## Core Value Proposition
Haunted Repo automates the tedious first pass of repo archaeology: instead of manually grepping for unused imports or re-running tests to find flakes, the tool does it systematically and produces actionable output.

## Scope Boundaries

### In Scope
- Public GitHub repositories
- Python codebases (3.8+)
- Read-only analysis by default
- Opt-in PR generation on user's fork

### Out of Scope
- Private repositories (no auth flow for MVP)
- Non-Python languages
- Auto-merging PRs (too risky)
- Paid vulnerability APIs
- Repository hosting (only analyze, not store)

## Success Metrics
- Correctly identifies known dead code in demo victims
- Detects flaky tests that flip on re-run
- Flags dependencies with known CVEs
- Generates valid markdown plan
- Opens PR that passes CI (on demo victims)
