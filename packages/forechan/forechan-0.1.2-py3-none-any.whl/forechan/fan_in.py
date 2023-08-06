from asyncio.tasks import gather
from typing import MutableSequence, TypeVar

from ._da import race
from .chan import chan
from .go import GO, go
from .ops import with_aclosing
from .types import Chan

T = TypeVar("T")


async def fan_in(*cs: Chan[T], cascade_close: bool = True, go: GO = go) -> Chan[T]:
    """
    # each item in `*cs` goes to `out`

    `*cs`
    ------>|
    ------>|
    ------>|---> `out`
    ------>|
    ------>|
    ...
    """

    out: Chan[T] = chan()
    channels: MutableSequence[Chan[T]] = [*cs]

    async def cont() -> None:
        async with out:
            async with with_aclosing(*cs, close=cascade_close):
                while out and channels:
                    (ready, _), _ = await gather(
                        race(*(ch._on_recvable() for ch in channels)),
                        out._on_sendable(),
                    )
                    if not ready:
                        channels[:] = [ch for ch in channels if ch]
                    elif ready.recvable() and out.sendable():
                        out.try_send(ready.try_recv())

    await go(cont())
    return out
