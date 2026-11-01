__all__ = ["public_api"]


def public_api():
    return helper()


def helper():
    return 1


def forgotten():
    return "nobody calls me"


class OldThing:
    pass
