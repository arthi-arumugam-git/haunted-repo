# Haunted Repo

Find and exorcise dead code, flaky tests, and cursed dependencies in abandoned Python repositories.

## Kiroween 2026

This project is a submission for [Kiroween 2026](https://kiroween.devpost.com/).

**Categories:**
- **Resurrection** (primary): Revives abandoned Python repos by identifying and fixing rot
- **Costume Contest** (secondary): Spooky graveyard UI with tombstones, ghosts, and skulls
- **Best Startup Project**: Addresses a real problem for open source maintainers

## What It Does

Haunted Repo analyzes a public GitHub repository and finds:

- **Zombies** (dead code): Modules and functions with no references and no test coverage
- **Poltergeists** (flaky tests): Tests that pass sometimes and fail other times
- **Cursed dependencies**: Packages with CVEs, EOL status, or outdated versions

It then generates a ranked Resurrection Plan with effort estimates and suggested fixes.

## How to Run

### Requirements

- Python 3.11+
- pip or uv

### Install

```bash
# Clone the repo
git clone https://github.com/arthi-arumugam-git/haunted-repo.git
cd haunted-repo

# Install dependencies
pip install -e ".[dev]"
```

### Run the app

```bash
uvicorn web.app:app --reload
```

Then open http://localhost:8000 to see the graveyard UI.

### Health check

```bash
curl http://localhost:8000/health
# {"status":"ok","service":"haunted-repo","version":"0.1.0"}
```

### Run tests

```bash
pytest
```

## Project Structure

```
haunted-repo/
├── .kiro/                    # Kiro project structure (specs, steering, hooks)
├── haunted/                  # Main Python package
│   ├── analyzer/             # Dead code detection
│   ├── flakes/               # Flaky test detection
│   ├── deps/                 # Dependency auditing
│   └── planner/              # Resurrection plan generation
├── web/                      # FastAPI application
│   ├── static/               # CSS
│   └── templates/            # Jinja2 templates
├── tests/                    # Test suite
├── pyproject.toml            # Project config
└── LICENSE                   # MIT
```

## How Kiro Is Used

The `.kiro/` folder at the repo root contains the Kiro project structure:

- **specs/haunted-repo/**: EARS-style requirements, design document, and task breakdown
- **steering/**: Product scope, technical decisions, and project structure guidelines
- **hooks/**: Agent hook configurations for on-save testing and flake detection

This structure was authored manually during Day 1 scaffolding. The build will continue using Kiro IDE features (agent hooks, experimentation, MCP integrations) as modules become functional.

## Code Quality

Quality gates planned for CI:
- **ruff**: Fast Python linter
- **bandit**: Security issue scanner
- **pytest**: Test suite with `pytest-randomly` and `pytest-repeat`

## Demo Victims

For testing, the project uses these abandoned repos:
1. [mbianchidev/corn-test](https://github.com/mbianchidev/corn-test) - Flaky test demo
2. [box/flaky](https://github.com/box/flaky) - Dead code + outdated deps demo

## License

MIT License. See [LICENSE](LICENSE).
