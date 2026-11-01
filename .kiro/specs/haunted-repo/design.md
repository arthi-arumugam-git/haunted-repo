# Design: Haunted Repo

## Components
- `haunted/analyzer` – ast reference graph; returns `Zombie(path, name, kind, lineno)` records.
- `haunted/flakes` – runs `pytest -p randomly` N times, diffs per-test outcomes.
- `haunted/deps` – reads requirements/pyproject, batches OSV `/v1/querybatch`.
- `haunted/planner` – merges findings into a ranked markdown plan.
- `haunted/web.py` – graveyard UI (static HTML via `scan --html`): tombstones for zombies, ghosts for poltergeists.

## Data flow
scan(path) -> analyzer + flakes + deps -> Findings -> planner -> RESURRECTION_PLAN.md (+ optional fork PR)

## Error handling
Unparseable files and failing installs are reported, never fatal.

## Testing
Each component has a fixture repo under `tests/fixtures/` with known answers.
