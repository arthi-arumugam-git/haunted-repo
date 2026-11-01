from pathlib import Path

from haunted.analyzer import scan

FIXTURE = Path(__file__).parent / "fixtures" / "victim"


def test_finds_known_zombies_only():
    names = {z.name for z in scan(FIXTURE).zombies}
    assert names == {"forgotten", "OldThing"}


def test_skips_unparseable_file():
    res = scan(FIXTURE)
    assert "broken.py" in res.skipped
