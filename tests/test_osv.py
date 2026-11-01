from pathlib import Path

import haunted.__main__ as cli
from haunted.analyzer import ScanResult
from haunted.osv import OSV_API, Dep, audit, find_deps, parse_pin
from haunted.planner import render_plan

FIX = Path(__file__).parent / "fixtures" / "cursed"

VULNS = {
    "PYSEC-2019-217": {"id": "PYSEC-2019-217", "summary": "Sandbox escape", "aliases": ["CVE-2019-10906"]},
    "GHSA-462w": {"id": "GHSA-462w", "summary": "Sandbox escape", "aliases": ["PYSEC-2019-217"]},
    "GHSA-xxxx": {"id": "GHSA-xxxx", "summary": "", "aliases": []},
    "PYSEC-2020-96": {"id": "PYSEC-2020-96", "summary": "Arbitrary code execution", "aliases": ["CVE-2020-1747"]},
}


class FakeOSV:
    def __init__(self, affected):
        self.affected = affected
        self.calls = []

    def __call__(self, url, body):
        self.calls.append((url, body))
        if url != f"{OSV_API}/querybatch":
            return VULNS[url.rsplit("/", 1)[1]]
        results = []
        for q in body["queries"]:
            ids = self.affected.get(q["package"]["name"], [])
            results.append({"vulns": [{"id": i} for i in ids]} if ids else {})
        return {"results": results}


def test_parse_pin():
    assert parse_pin("Jinja2==2.10") == ("jinja2", "2.10")
    assert parse_pin("zope.interface[test] == 5.0 ; python_version>'3'") == ("zope-interface", "5.0")
    assert parse_pin("flask>=1.0") is None
    assert parse_pin("django==2.*") is None
    assert parse_pin("attrs==23.1.0,<24") is None


def test_find_deps_reads_requirements_and_pyproject():
    deps = find_deps(FIX)
    assert deps == [
        Dep("pytest", "8.0.0", "requirements-dev.txt"),
        Dep("jinja2", "2.10", "requirements-dev.txt"),
        Dep("requests", "2.19.0", "requirements.txt"),
        Dep("pyyaml", "5.3", "pyproject.toml"),
    ]


def test_audit_returns_only_vulnerable_deps():
    fake = FakeOSV({"jinja2": ["PYSEC-2019-217", "GHSA-xxxx"], "pyyaml": ["PYSEC-2020-96"]})
    cursed = audit(FIX, http=fake)
    assert [(c.dep.name, [v.id for v in c.vulns]) for c in cursed] == [
        ("jinja2", ["PYSEC-2019-217", "GHSA-xxxx"]),
        ("pyyaml", ["PYSEC-2020-96"]),
    ]
    assert cursed[0].vulns[0].aliases == ("CVE-2019-10906",)
    batch = fake.calls[0][1]["queries"]
    assert {"package": {"name": "jinja2", "ecosystem": "PyPI"}, "version": "2.10"} in batch


def test_audit_drops_aliased_duplicates():
    cursed = audit(FIX, http=FakeOSV({"jinja2": ["GHSA-462w", "PYSEC-2019-217"]}))
    assert [v.id for v in cursed[0].vulns] == ["GHSA-462w"]


def test_audit_skips_network_without_pins(tmp_path):
    fake = FakeOSV({})
    assert audit(tmp_path, http=fake) == []
    assert fake.calls == []


def test_plan_has_cursed_section():
    cursed = audit(FIX, http=FakeOSV({"pyyaml": ["PYSEC-2020-96"]}))
    plan = render_plan("cursed", ScanResult(), cursed=cursed)
    assert "## Cursed dependencies" in plan
    assert "`pyyaml==5.3` in `pyproject.toml`" in plan
    assert "`PYSEC-2020-96` (CVE-2020-1747): Arbitrary code execution" in plan


def test_cli_no_osv_skips_audit(monkeypatch, capsys):
    def boom(root):
        raise AssertionError("audit should not run")
    monkeypatch.setattr(cli, "audit", boom)
    assert cli.main(["scan", str(FIX), "--no-osv"]) == 0
    assert "Cursed" not in capsys.readouterr().out


def test_cli_reports_osv_failure_and_continues(monkeypatch, capsys):
    def offline(root):
        raise OSError("no network")
    monkeypatch.setattr(cli, "audit", offline)
    assert cli.main(["scan", str(FIX)]) == 0
    out = capsys.readouterr()
    assert "Resurrection plan" in out.out
    assert "OSV lookup failed" in out.err
