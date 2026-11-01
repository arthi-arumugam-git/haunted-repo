"""Render scan findings as a single self-contained HTML graveyard page."""
from __future__ import annotations

from html import escape

from haunted.analyzer import ScanResult
from haunted.osv import CursedDep

_CSS = """
:root { --bg: #111316; --card: #1a1d21; --line: #2a2e34; --text: #d7dade; --muted: #8a9099; --accent: #9fd18b; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
main { max-width: 1040px; margin: 0 auto; padding: 40px 24px 64px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 40px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--line); }
.count { color: var(--accent); font-variant-numeric: tabular-nums; }
.summary { color: var(--muted); margin: 0; }
.grid { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); }
.card { background: var(--card); border: 1px solid var(--line); padding: 14px 16px; min-width: 0; }
.tomb { border-radius: 48px 48px 4px 4px; padding-top: 22px; text-align: center; }
.ghost { border-radius: 14px 14px 2px 2px; border-bottom: 2px dashed var(--line); }
.name { font-weight: 600; overflow-wrap: anywhere; }
.meta, .empty { color: var(--muted); font-size: 13px; overflow-wrap: anywhere; }
.kind { display: inline-block; margin-top: 6px; font-size: 12px; color: var(--accent);
  border: 1px solid var(--line); border-radius: 3px; padding: 0 6px; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
.vulns { margin: 8px 0 0; padding-left: 18px; font-size: 13px; }
.vulns li { margin: 2px 0; }
"""


def _section(title: str, count: int, empty: str, cards: list[str]) -> str:
    head = f'<h2>{escape(title)} <span class="count">({count})</span></h2>'
    if not cards:
        return f'<section>{head}<p class="empty">{escape(empty)}</p></section>'
    return f'<section>{head}<ul class="grid">{"".join(cards)}</ul></section>'


def render_html(
    repo: str,
    result: ScanResult,
    poltergeists: list[str] | None = None,
    cursed: list[CursedDep] | None = None,
) -> str:
    poltergeists = poltergeists or []
    cursed = cursed or []
    zombies = sorted(result.zombies, key=lambda z: (z.path, z.lineno))

    tombs = [
        f'<li class="card tomb"><div class="name"><code>{escape(z.name)}</code></div>'
        f'<div class="meta">{escape(z.path)}:{z.lineno}</div>'
        f'<span class="kind">{escape(z.kind)}</span></li>'
        for z in zombies
    ]
    ghosts = [
        f'<li class="card ghost"><div class="name"><code>{escape(t)}</code></div>'
        f'<div class="meta">result changes with run order</div></li>'
        for t in poltergeists
    ]
    curses = []
    for c in cursed:
        ids = "".join(
            f"<li><code>{escape(v.id)}</code>"
            + (f' <span class="meta">{escape(", ".join(v.aliases))}</span>' if v.aliases else "")
            + "</li>"
            for v in c.vulns
        )
        curses.append(
            f'<li class="card"><div class="name"><code>{escape(c.dep.name)}=={escape(c.dep.version)}</code></div>'
            f'<div class="meta">{escape(c.dep.source)}</div><ul class="vulns">{ids}</ul></li>'
        )
    broken = [
        f'<li class="card"><div class="name"><code>{escape(path)}</code></div>'
        f'<div class="meta">{escape(why)}</div></li>'
        for path, why in sorted(result.skipped.items())
    ]

    sections = [
        _section("Zombies: unreferenced code", len(tombs), "No unreferenced functions or classes found.", tombs),
        _section("Poltergeists: order-dependent tests", len(ghosts),
                 "No flaky tests found (or the flake hunt was not run).", ghosts),
        _section("Cursed dependencies: known vulnerabilities", len(curses),
                 "No pinned dependencies with known vulnerabilities (or the OSV lookup was skipped).", curses),
    ]
    if broken:
        sections.insert(0, _section("Unparseable files", len(broken), "", broken))

    total = len(tombs) + len(ghosts) + len(curses) + len(broken)
    title = f"Graveyard for {repo}"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{escape(title)}</title><style>{_CSS}</style></head><body><main>"
        f"<h1>{escape(title)}</h1>"
        f'<p class="summary"><span class="count">{total}</span> findings: {len(tombs)} zombies, '
        f"{len(ghosts)} poltergeists, {len(curses)} cursed dependencies.</p>"
        f"{''.join(sections)}</main></body></html>\n"
    )
