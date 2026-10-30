# Technical Steering

## Language & Runtime
- Python 3.11+ (required for modern typing features)
- FastAPI for backend (async support, automatic OpenAPI docs)

## Testing Stack
- pytest as test runner
- pytest-randomly for test order randomization
- pytest-repeat for multi-run flake detection
- Coverage.py for coverage measurement

## Code Analysis
- stdlib `ast` module for Python parsing and reference graphs
- vulture as optional cross-check for dead code
- No paid static analysis tools

## Dependency Auditing
- pip-audit for local vulnerability scanning
- OSV API (https://osv.dev) for CVE lookups (free, no auth required)
- PyPI JSON API for version freshness checks

## Code Quality Gates
Run before every commit:
- **ruff**: Fast Python linter (replaces flake8, isort, etc.)
- **bandit**: Security issue scanner
- Document these in CI; wire them if time permits

## Anti-Slop Policy
- No filler marketing copy in UI or README
- No em-dash spam in prose
- Plain language, direct statements
- UI text reviewed for AI-generated tells

## External APIs
- GitHub API (public, no auth for read operations on public repos)
- OSV API (free vulnerability database)
- PyPI JSON API (package metadata)

## No Paid Services
- No OpenAI/Anthropic API calls for MVP
- No paid GitHub features
- No commercial vulnerability databases
