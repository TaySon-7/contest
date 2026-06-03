import pytest
from src.task2 import cached_method


def test_init():
    class Report:
        def __init__(self):
            self.calls = 0

        @cached_method
        def total(self):
            self.calls += 1
            return 10

    report = Report()

    assert report.total() == 10
    assert report.total() == 10
    assert report.calls == 1


def test_reset_after_init():
    class Report:
        def __init__(self):
            self.calls = 0

        @cached_method
        def total(self):
            self.calls += 1
            return 10

    report = Report()

    assert report.total() == 10
    assert report.total() == 10
    assert report.calls == 1
    Report.total.reset(report)
    assert report.total() == 10
    assert report.calls == 2