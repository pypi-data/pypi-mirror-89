from asyncio.tasks import gather
from contextlib import asynccontextmanager
from typing import AsyncIterable, AsyncIterator, Iterable, TypeVar, Union, cast

from .chan import chan
from .go import GO, go
from .types import AsyncClosable, Chan

T = TypeVar("T")


async def to_chan(it: Union[Iterable[T], AsyncIterable[T]], go: GO = go) -> Chan[T]:
    """
    Iterable[T] / AsyncIterable[T] -> Chan[T]
    """

    ch: Chan[T] = chan()

    async def gen() -> AsyncIterator[T]:
        for item in cast(Iterable[T], it):
            yield item

    ait = gen() if isinstance(it, Iterable) else it

    async def cont() -> None:
        async with ch:
            async for item in ait:
                while ch:
                    await ch._on_sendable()
                    if ch.sendable():
                        ch.try_send(item)
                        break
                if not ch:
                    break

    await go(cont())
    return ch


@asynccontextmanager
async def with_aclosing(
    *closables: AsyncClosable, close: bool = True
) -> AsyncIterator[None]:
    """
    async with with_closing(*cs):
        ...
    # close each `chan` in *cs after block
    """

    try:
        yield None
    finally:
        if close:
            await gather(*(c.aclose() for c in closables))
