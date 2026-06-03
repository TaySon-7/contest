from typing import Iterable
from collections import deque


class HistoryCapError(ValueError):
    pass


class RewindableStream:
    def __init__(self, source: Iterable[object], capacity: int) -> None:
        if capacity < 0:
            raise ValueError("вместимость должна быть больше нуля")
        self._cap = capacity
        self._iter = iter(source)
        self._history = deque(maxlen=capacity)
        self._rep = deque()

    def __iter__(self) -> object:
        return self

    def __next__(self) -> object:
        if self._rep:
            return self._rep.popleft()

        value = next(self._iter)
        if self._cap > 0:
            self._history.append(value)

        return value

    def rewind(self, steps: int = 1) -> None:
        if steps == 0:
            return
        if steps < 0:
            raise ValueError("Количество шагов должно быть больше нуля")
        if steps > len(self._history):
            raise HistoryCapError("Количество шагов не должно превышать длину самой истории")
        values = list(self._history)

        for value in values[-steps:]:
            self._rep.append(value)
