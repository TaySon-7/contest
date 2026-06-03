from typing import AsyncIterator, AsyncIterable

class AsyncBatcher:
    def __init__(self, source: AsyncIterable[object] | AsyncIterator[object], size: int) -> None:
        if size <= 0:
            raise ValueError("Длина должна быть больше нуля")
        self._source = source
        self._iter = source.__aiter__()
        self._closed = False
        self._size = size

    def __aiter__(self) -> AsyncIterator[list[object]]:
        return self._iterator()

    async def _iterator(self) -> AsyncIterator[list[object]]:
        try:
            while True:
                yield await self.__anext__()
        except StopAsyncIteration:
            return
        finally:
            await self.aclose()

    async def __anext__(self) -> list[object]:
        if self._closed:
            raise StopAsyncIteration
        batch = []
        while len(batch) < self._size:
            try:
                item = await self._iter.__anext__()
            except StopAsyncIteration:
                self._closed = True
                if batch:
                    return batch
                raise
            batch.append(item)
        return batch

    async def aclose(self) -> None:
        if self._closed:
            return
        self._closed = True
        close = getattr(self._iter, "aclose", None)
        if close is not None:
            result = close()
            if result is not None:
                await result
