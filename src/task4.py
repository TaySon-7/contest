from typing import Protocol, Iterable
from types import TracebackType


class ContextManager(Protocol):
    def __enter__(self) -> object:
        ...

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None,) -> bool | None:
        ...


class SafeContextStack:
    def __init__(self, managers: Iterable[ContextManager]) -> None:
        self._managers = list(managers)
        self._entered: list[ContextManager] = []

    def __enter__(self) -> list[object]:
        res = []
        try:
            for man in self._managers:
                res.append(man.__enter__())
                self._entered.append(man)
        except BaseException as err:
            self._close(type(err), err, err.__traceback__)
            raise

        return res

    def _close(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None, ) -> bool:
        flag = False
        last_error = None
        last_tb = None
        while self._entered:
            man = self._entered.pop()
            try:
                if man.__exit__(exc_type, exc, tb):
                    flag = True
                    exc_type = None
                    exc = None
                    tb = None
            except BaseException as err:
                last_error = err
                last_tb = err.__traceback__
                exc_type = type(err)
                exc = err
                tb = last_tb
                flag = False
        if last_error is not None:
            raise last_error.with_traceback(last_tb)
        return flag


    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None,) -> bool:
        return self._close(exc_type, exc, tb)

