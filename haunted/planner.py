"""Turn scan findings into a ranked markdown resurrection plan (Req 4.1)."""
from __future__ import annotations

from haunted.analyzer import ScanResult
from haunted.osv import CursedDep

# Lower effort first: a skipped (unparseable) file blocks every other check,
# so it ranks above dead code.
def render_plan(
    repo: str,
    result: ScanResult,
    poltergeists: list[str] | None = None,
    cursed: list[CursedDep] | None = None,
) -> str:
    poltergeists = poltergeists or []
    cursed = cursed or []
    lines = [f"# Resurrection plan for `{repo}`", ""]
    if not result.skipped and not result.zombies and not poltergeists and not cursed:
        lines.append("No findings. This repo is resting peacefully.")
        return "\n".join(lines) + "\n"
    step = 1
    if result.skipped:
        lines += ["## Fix first: files that do not parse", ""]
        for path, why in sorted(result.skipped.items()):
            lines.append(f"{step}. `{path}`: {why}. Risk high, effort low.")
            step += 1
        lines.append("")
    if cursed:
        lines += ["## Cursed dependencies: pinned versions with known vulnerabilities", ""]
        for c in cursed:
            lines.append(f"{step}. `{c.dep.name}=={c.dep.version}` in `{c.dep.source}` has {len(c.vulns)} known "
                         f"vulnerabilities. Risk high, effort low.")
            for v in c.vulns:
                aliases = f" ({', '.join(v.aliases)})" if v.aliases else ""
                lines.append(f"   - `{v.id}`{aliases}: {v.summary or 'no summary'}")
            step += 1
        lines.append("")
    if poltergeists:
        lines += ["## Next: tests whose result changes with run order", ""]
        for t in poltergeists:
            lines.append(f"{step}. `{t}` passed in some shuffled runs and failed in others. Risk high, effort medium.")
            step += 1
        lines.append("")
    if result.zombies:
        lines += ["## Then: unreferenced code to review or delete", ""]
        for z in sorted(result.zombies, key=lambda z: (z.kind != "class", z.path, z.lineno)):
            lines.append(f"{step}. `{z.path}:{z.lineno}` {z.kind} `{z.name}` has no references. Risk low, effort low.")
            step += 1
        lines.append("")
    return "\n".join(lines)
