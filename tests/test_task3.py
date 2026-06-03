import pytest
from src.task3 import RewindableStream



def test_rewind():
    stream = RewindableStream([1, 2, 3], capacity=2)
    assert next(stream) == 1
    assert next(stream) == 2
    stream.rewind()
    assert next(stream) == 2
    assert next(stream) == 3


def test_stop_iter():
    stream = RewindableStream([1, 2, 3, 4, 5], capacity=2)

    assert next(stream) == 1
    assert next(stream) == 2
    assert next(stream) == 3
    assert next(stream) == 4
    assert next(stream) == 5
    with pytest.raises(StopIteration):
        next(stream)