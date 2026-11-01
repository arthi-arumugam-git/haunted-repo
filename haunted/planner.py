"""Turn scan findings into a ranked markdown resurrection plan (Req 4.1)."""
from __future__ import annotations

from haunted.analyzer import ScanResult

# Lower effort first: a skipped (unparseable) file blocks every other check,
# so it ranks above dead code.
def render_plan(repo: str, result: ScanResult) -> str:
    lines = [f"# Resurrection plan for `{repo}`", ""]
    if not result.skipped and not result.zombies:
        lines.append("No findings. This repo is resting peacefully.")
        return "\n".join(lines) + "\n"
    step = 1
    if result.skipped:
        lines += ["## Fix first: files that do not parse", ""]
        for path, why in sorted(result.skipped.items()):
            lines.append(f"{step}. `{path}`: {why}. Risk high, effort low.")
            step += 1
        lines.append("")
    if result.zombies:
        lines += ["## Then: unreferenced code to review or delete", ""]
        for z in sorted(result.zombies, key=lambda z: (z.kind != "class", z.path, z.lineno)):
            lines.append(f"{step}. `{z.path}:{z.lineno}` {z.kind} `{z.name}` has no references. Risk low, effort low.")
            step += 1
        lines.append("")
    return "\n".join(lines)
