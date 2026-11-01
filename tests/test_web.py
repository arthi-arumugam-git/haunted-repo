from pathlib import Path

from haunted.__main__ import main
from haunted.analyzer import ScanResult, Zombie
from haunted.osv import CursedDep, Dep, Vuln
from haunted.web import render_html

FIXTURE = Path(__file__).parent / "fixtures" / "victim"


def _result():
    return ScanResult(zombies=[
        Zombie("pkg/a.py", "<script>alert(1)</script>", "function", 3),
        Zombie("pkg/b.py", "OldThing", "class", 10),
    ])


def test_escapes_all_text():
    cursed = [CursedDep(Dep("evil<pkg>", "1.0&2", "req's.txt"), [Vuln('GHSA-"x"', "s", ("CVE-<1>",))])]
    html = render_html("<repo>", _result(), ["tests/t.py::test_<b>"], cursed)
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "&lt;repo&gt;" in html
    assert "test_&lt;b&gt;" in html
    assert "evil&lt;pkg&gt;==1.0&amp;2" in html
    assert "req&#x27;s.txt" in html
    assert "GHSA-&quot;x&quot;" in html
    assert "CVE-&lt;1&gt;" in html


def test_cards_and_counts():
    cursed = [CursedDep(Dep("requests", "2.0.0", "requirements.txt"), [Vuln("GHSA-1", ""), Vuln("PYSEC-2", "")])]
    html = render_html("r", _result(), ["t::flaky"], cursed)
    assert html.count('class="card tomb"') == 2
    assert html.count('class="card ghost"') == 1
    assert "pkg/b.py:10" in html and ">class<" in html
    assert "requests==2.0.0" in html and "GHSA-1" in html and "PYSEC-2" in html
    assert 'Zombies: unreferenced code <span class="count">(2)</span>' in html
    assert 'Poltergeists: order-dependent tests <span class="count">(1)</span>' in html
    assert 'Cursed dependencies: known vulnerabilities <span class="count">(1)</span>' in html


def test_empty_states():
    html = render_html("r", ScanResult())
    assert html.count('class="empty"') == 3
    assert "No unreferenced functions or classes found." in html
    assert "No flaky tests found" in html
    assert "No pinned dependencies with known vulnerabilities" in html
    assert "Unparseable files" not in html


def test_self_contained():
    html = render_html("r", _result())
    assert html.startswith("<!DOCTYPE html>")
    assert "<script" not in html
    assert "http://" not in html and "https://" not in html
    assert "<link" not in html


def test_cli_writes_html(tmp_path):
    out = tmp_path / "graveyard.html"
    assert main(["scan", str(FIXTURE), "--no-osv", "-o", str(tmp_path / "plan.md"), "--html", str(out)]) == 0
    html = out.read_text()
    assert "Graveyard for victim" in html
    assert "forgotten" in html
    assert "Unparseable files" in html and "broken.py" in html
