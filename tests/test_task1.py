import pytest
from src.task1 import AttributeRouter

def test_init():
    class Config:
        host = "localhost"

    router = AttributeRouter(Config())

    assert router.host == "localhost"
    assert router.has_route("host") == True

def test_init_2():
    class A:
        value = 1

    class B:
        value = 2

    router = AttributeRouter(A(), B())

    assert router.value == 1


def test_wrong_attr():
    class A:
        value = 1

    router = AttributeRouter(A())
    with pytest.raises(AttributeError):
        print(router.attr)