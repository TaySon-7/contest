import pytest
from src.task4 import SafeContextStack

class MyContextManager:
    def __init__(self, name, log, enter_error=None, exit_error=None, flag=False):
        self.name = name
        self.log = log
        self.enter_error = enter_error
        self.exit_error = exit_error
        self.flag = flag

    def __enter__(self):
        self.log.append(f"enter {self.name}")

        if self.enter_error is not None:
            raise self.enter_error

        return f"resource {self.name}"

    def __exit__(self, exc_type, exc, tb):
        self.log.append(f"exit {self.name}")

        if self.exit_error is not None:
            raise self.exit_error

        return self.flag


def test_init():
    log = []
    with SafeContextStack(
            [MyContextManager("a", log), MyContextManager("b", log), MyContextManager("c", log)]) as resources:
        assert resources == ["resource a", "resource b", "resource c"]
        log.append("wait")

    assert log == ["enter a", "enter b", "enter c", "wait", "exit c", "exit b", "exit a"]



def test_exit_error():
    log = []

    first_error = RuntimeError("first")
    second_error = ValueError("second")

    with pytest.raises(ValueError) as error_info:
        with SafeContextStack([MyContextManager("a", log, exit_error=second_error), MyContextManager("b", log, exit_error=first_error)]):
            pass

    assert error_info.value is second_error
    assert log == ["enter a", "enter b", "exit b", "exit a"]