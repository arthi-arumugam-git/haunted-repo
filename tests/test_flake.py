from pathlib import Path

from haunted.flake import hunt

FIX = Path(__file__).parent / "fixtures" / "flaky"


def test_order_dependent_test_is_a_poltergeist():
    r = hunt(FIX, runs=8, seed=1)
    names = [p.split("::")[-1] for p in r.poltergeists]
    assert "test_reader_depends_on_writer" in names
    assert "test_stable" not in names
    assert "test_writer" not in names
