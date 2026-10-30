# Project Structure Steering

## Directory Layout

```
haunted-repo/
├── .kiro/                    # Kiro project structure (committed, not gitignored)
│   ├── specs/
│   │   └── haunted-repo/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   ├── steering/
│   │   ├── product.md
│   │   ├── tech.md
│   │   └── structure.md
│   └── hooks/
│       └── hooks.md
├── haunted/                  # Main Python package
│   ├── __init__.py
│   ├── analyzer/             # Dead code detection
│   │   ├── __init__.py
│   │   └── graph.py
│   ├── flakes/               # Flaky test detection
│   │   ├── __init__.py
│   │   └── runner.py
│   ├── deps/                 # Dependency auditing
│   │   ├── __init__.py
│   │   └── audit.py
│   └── planner/              # Resurrection plan generation
│       ├── __init__.py
│       └── plan.py
├── web/                      # FastAPI application
│   ├── __init__.py
│   ├── app.py                # FastAPI app entry point
│   ├── static/               # CSS, JS
│   │   └── style.css
│   └── templates/            # Jinja2 templates
│       ├── base.html
│       └── graveyard.html
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_flakes.py
│   ├── test_deps.py
│   └── test_planner.py
├── pyproject.toml            # Project config and dependencies
├── README.md
├── LICENSE                   # MIT
└── .gitignore                # Does NOT ignore .kiro/
```

## Module Responsibilities

### haunted/analyzer
Owns AST parsing, import graph construction, and dead code identification.

### haunted/flakes
Owns pytest subprocess execution, result comparison, and flake detection.

### haunted/deps
Owns dependency file parsing, OSV/PyPI API calls, and vulnerability flagging.

### haunted/planner
Owns aggregation of findings, ranking logic, and markdown generation.

### web/
Owns HTTP endpoints, HTML rendering, and user interaction.

### tests/
Mirrors the haunted/ structure with corresponding test modules.

## Naming Conventions
- Modules: lowercase, underscore-separated
- Classes: PascalCase
- Functions: lowercase, underscore-separated
- Constants: UPPERCASE_WITH_UNDERSCORES
