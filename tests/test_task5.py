import pytest
from src.task5 import AsyncBatcher


async def async_source(values):
    for value in values:
        yield value


async def collect_batches(source, size):
    batches = []
    async for batch in AsyncBatcher(source, size):
        batches.append(batch)
    return batches

@pytest.mark.asyncio
async def test_init():
    assert await collect_batches(async_source([1, 2, 3, 4, 5]), 2) == [[1, 2], [3, 4], [5]]


@pytest.mark.asyncio
async def test_stop_iter():
    batcher = AsyncBatcher(async_source([1]), 2)
    assert await batcher.__anext__() == [1]
    with pytest.raises(StopAsyncIteration):
        await batcher.__anext__()
