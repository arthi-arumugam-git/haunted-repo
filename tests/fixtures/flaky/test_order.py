STATE = {}


def test_writer():
    STATE["ready"] = True


def test_reader_depends_on_writer():
    assert STATE.get("ready")


def test_stable():
    assert 1 + 1 == 2
