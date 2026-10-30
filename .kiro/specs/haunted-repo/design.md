# Haunted Repo: Design Document

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Web UI (Graveyard)                       │
│   - Tombstones = zombie modules                              │
│   - Ghosts = flaky tests                                     │
│   - Skulls = cursed dependencies                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    FastAPI Backend                           │
│   /            → Graveyard UI                                │
│   /health      → Health check                                │
│   /api/analyze → Trigger full analysis                       │
│   /api/status  → Check analysis status                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   Analyzer    │ │    Flakes     │ │     Deps      │
│ (zombie code) │ │ (poltergeist) │ │   (cursed)    │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                ┌───────────────────┐
                │      Planner      │
                │ (resurrection md) │
                └───────────────────┘
```

## Component Design

### haunted/analyzer
- Builds Python AST-based module dependency graph
- Uses stdlib `ast` module for parsing
- Cross-checks with vulture-style reference analysis
- Identifies unreachable code via graph traversal

### haunted/flakes
- Runs pytest with `pytest-randomly` and `pytest-repeat`
- Executes N runs (configurable, default 5)
- Compares results across runs to detect non-determinism
- Reports tests that flip between pass/fail

### haunted/deps
- Parses requirements.txt, setup.py, pyproject.toml
- Queries OSV API for known vulnerabilities
- Checks PyPI for version freshness
- Flags EOL packages via maintained package lists

### haunted/planner
- Aggregates findings from all analyzers
- Ranks issues by severity and fix effort
- Generates markdown resurrection plan
- Can generate PR diff for automated fixes

### web/
- FastAPI application serving the graveyard UI
- Jinja2 templates with spooky styling
- Real-time status updates via polling
- Results displayed as tombstones (zombies), ghosts (flaky), skulls (deps)

## Data Flow

1. User submits GitHub URL via UI
2. Backend clones repo to sandbox
3. Parallel analysis: analyzer, flakes, deps
4. Planner aggregates and ranks findings
5. UI renders graveyard with findings
6. Optional: Generate PR via GitHub MCP

## Technology Stack

- Python 3.11+
- FastAPI for backend
- Jinja2 for templates
- pytest + pytest-randomly + pytest-repeat for flake detection
- ast (stdlib) for code analysis
- httpx for GitHub/OSV API calls
- ruff + bandit for code quality gates
