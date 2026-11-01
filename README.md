# Haunted Repo

Finds dead code, flaky tests, and vulnerable dependencies in abandoned Python repos, then writes a ranked plan to bring them back. Built for Kiroween 2026 with Kiro specs, steering, and hooks (see `.kiro/`).

```
python -m pytest
```

## Opening a PR on your fork

`scan --open-pr` commits the plan as `RESURRECTION_PLAN.md` on a branch named `haunted/resurrection-plan`, pushes it to `origin`, and opens one PR with `gh`. It only works when `origin` is owned by the account `gh` is logged in as, so it never opens PRs on someone else's repo. It never merges.

Without `--yes` it is a dry run: it prints the exact `git` and `gh` commands and changes nothing. `--dry-run-pr` forces a dry run even with `--yes`.

```
python -m haunted scan path/to/fork -o plan.md --open-pr        # print commands
python -m haunted scan path/to/fork -o plan.md --open-pr --yes  # run them
```

Needs `git` and an authenticated `gh` (`gh auth login`). The dry run still calls `gh` to check who owns the repo.
