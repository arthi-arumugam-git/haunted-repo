from pathlib import Path

from haunted.analyzer import scan

FIXTURE = Path(__file__).parent / "fixtures" / "victim"


def test_finds_known_zombies_only():
    names = {z.name for z in scan(FIXTURE).zombies}
    assert names == {"forgotten", "OldThing"}


def test_skips_unparseable_file():
    res = scan(FIXTURE)
    assert "broken.py" in res.skipped


def _zombie_names(tmp_path, files):
    for name, src in files.items():
        (tmp_path / name).write_text(src)
    return {z.name for z in scan(tmp_path).zombies}


def test_ignores_pytest_test_classes_and_functions(tmp_path):
    names = _zombie_names(tmp_path, {
        "test_plugin.py": "class TestFlakyPlugin:\n    def test_reruns(self):\n        pass\n\ndef test_thing():\n    pass\n",
    })
    assert names == set()


def test_ignores_unittest_testcase_subclasses(tmp_path):
    names = _zombie_names(tmp_path, {
        "test_units.py": "import unittest\nfrom unittest import TestCase\n\n"
        "class PluginChecks(unittest.TestCase):\n    pass\n\nclass MoreChecks(TestCase):\n    pass\n",
    })
    assert names == set()


def test_ignores_pytest_hooks(tmp_path):
    names = _zombie_names(tmp_path, {
        "conftest.py": "def pytest_generate_tests(metafunc):\n    pass\n\ndef pytest_configure(config):\n    pass\n",
    })
    assert names == set()


def test_ignores_pytest_fixtures(tmp_path):
    names = _zombie_names(tmp_path, {
        "conftest.py": "import pytest\nfrom pytest import fixture\n\n"
        "@pytest.fixture\ndef my_fixture():\n    return 1\n\n"
        "@pytest.fixture(scope='session')\ndef session_thing():\n    return 2\n\n"
        "@fixture\ndef bare_fixture():\n    return 3\n",
    })
    assert names == set()


def test_still_reports_unreferenced_code_beside_tests(tmp_path):
    names = _zombie_names(tmp_path, {
        "conftest.py": "import pytest\n\n@pytest.fixture\ndef my_fixture():\n    return 1\n\n"
        "def helper():\n    pass\n\nclass Ghost:\n    pass\n",
    })
    assert names == {"helper", "Ghost"}
