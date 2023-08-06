from math import log10

__version__ = "0"


def percentile(nines: int):
    assert nines >= 0
    return 1. - (10 ** -nines)


def nines(p: float):
    assert 0 <= p < 1
    return -log10(1. - p)
