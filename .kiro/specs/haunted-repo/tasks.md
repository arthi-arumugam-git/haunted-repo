# Haunted Repo: Task Breakdown

## Day 1: Scaffold (Oct 30-31)

- [x] Create public GitHub repo with MIT license
- [x] Set up .kiro/ folder structure (specs, steering, hooks)
- [x] Author requirements.md from EARS planning notes
- [x] Author design.md with architecture
- [x] Create package layout (haunted/*, web/, tests/)
- [x] Implement minimal FastAPI app with health endpoint
- [x] Create graveyard UI skeleton (static placeholder)
- [x] Add stub modules for analyzer, flakes, deps, planner
- [x] Write README with categories and run instructions
- [x] Configure pyproject.toml with dependencies
- [x] Create .gitignore (excluding .kiro/)
- [ ] Open PR for Day-1 scaffold

## Day 2-3: Analyzer Module

- [ ] Implement AST parser for Python modules
- [ ] Build import graph from parsed modules
- [ ] Detect unreferenced modules (zombies)
- [ ] Detect unreferenced functions within modules
- [ ] Add test coverage check integration
- [ ] Write unit tests for analyzer
- [ ] Integrate analyzer API endpoint

## Day 4-5: Flakes Module

- [ ] Implement pytest subprocess runner
- [ ] Add pytest-randomly configuration
- [ ] Implement multi-run comparison logic
- [ ] Detect pass/fail flips across runs
- [ ] Store run history for evidence
- [ ] Write unit tests for flake detection
- [ ] Integrate flakes API endpoint

## Day 6-7: Deps Module

- [ ] Implement requirements.txt parser
- [ ] Implement pyproject.toml parser
- [ ] Add OSV API integration for CVE lookup
- [ ] Add PyPI version freshness check
- [ ] Implement EOL package detection
- [ ] Write unit tests for deps module
- [ ] Integrate deps API endpoint

## Day 8-9: Planner & PR Generation

- [ ] Implement finding aggregation
- [ ] Add severity/effort ranking logic
- [ ] Generate markdown resurrection plan
- [ ] Implement PR diff generation
- [ ] Add GitHub MCP integration for PR creation
- [ ] Write tests for planner

## Day 10-12: UI Polish & Demo

- [ ] Design spooky graveyard CSS
- [ ] Implement tombstone components for zombies
- [ ] Implement ghost animations for flaky tests
- [ ] Implement skull icons for cursed deps
- [ ] Add real-time status updates
- [ ] Test on demo victims (corn-test, box/flaky)
- [ ] Record demo video
- [ ] Write Devpost submission
