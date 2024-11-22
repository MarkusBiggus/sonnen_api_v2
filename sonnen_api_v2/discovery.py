import asyncio
import logging
import sys
from asyncio import Future, Task
from collections import defaultdict
from typing import Dict, Literal, Sequence, Set, Type, TypedDict, Union, cast

from sonnen_api_v2 import Sonnen as SonnenBatterie
#from solax.batterie_http_client import SonnenBatterieHttpClient

__all__ = ("discover", "DiscoveryKeywords", "DiscoveryError")

#from importlib.metadata import entry_points

from typing import Unpack

# registry of batteries
# REGISTRY: Set[Type[SonnenBatterie]] = {
#     ep.load()
#     for ep in entry_points(group="solax.batterie")
#     if issubclass(ep.load(), SonnenBatterie)
# }

logging.basicConfig(level=logging.INFO)


class DiscoveryKeywords(TypedDict, total=False):
    batteries: Sequence[Type[SonnenBatterie]]
    return_when: Literal["ALL_COMPLETED", "FIRST_COMPLETED"]


if sys.version_info >= (3, 9):
    _SonnenBatterieTask = Task[SonnenBatterie]
else:
    _SonnenBatterieTask = Task


class _DiscoveryHttpClient:
    def __init__(
        self,
        batterie: SonnenBatterie,
        http_client: SonnenBatterieHttpClient,
        request: Future,
    ):
        self._batterie = batterie
        self._http_client = http_client
        self._request: Future = request

    def __str__(self):
        return str(self._http_client)

    async def request(self):
        request = await self._request
        request.add_done_callback(self._restore_http_client)
        return await request

    def _restore_http_client(self, _: _SonnenBatterieTask):
        self._batterie.http_client = self._http_client


async def _discovery_task(i) -> SonnenBatterie:
    logging.info("Trying batterie %s", i)
    await i.get_data()
    return i


async def discover(
    host, port, pwd="", **kwargs: Unpack[DiscoveryKeywords]
) -> Union[SonnenBatterie, Set[SonnenBatterie]]:
    done: Set[_SonnenBatterieTask] = set()
    pending: Set[_SonnenBatterieTask] = set()
    failures = set()
    requests: Dict[SonnenBatterieHttpClient, Future] = defaultdict(
        asyncio.get_running_loop().create_future
    )

    return_when = kwargs.get("return_when", asyncio.FIRST_COMPLETED)
    for cls in kwargs.get("batteries", REGISTRY):
        for batterie in cls.build_all_variants(host, port, pwd):
            batterie.http_client = cast(
                SonnenBatterieHttpClient,
                _DiscoveryHttpClient(
                    batterie, batterie.http_client, requests[batterie.http_client]
                ),
            )

            pending.add(
                asyncio.create_task(_discovery_task(batterie), name=f"{batterie}")
            )

    if not pending:
        raise DiscoveryError("No batteries to try to discover")

    def cancel(pending: Set[_SonnenBatterieTask]) -> Set[_SonnenBatterieTask]:
        for task in pending:
            task.cancel()
        return pending

    def remove_failures_from(done: Set[_SonnenBatterieTask]) -> None:
        for task in set(done):
            exc = task.exception()
            if exc:
                failures.add(exc)
                done.remove(task)

    # stagger HTTP request to prevent accidental Denial Of Service
    async def stagger() -> None:
        for http_client, future in requests.items():
            future.set_result(asyncio.create_task(http_client.request()))
            await asyncio.sleep(1)

    staggered = asyncio.create_task(stagger())

    while pending and (not done or return_when != asyncio.FIRST_COMPLETED):
        try:
            done, pending = await asyncio.wait(pending, return_when=return_when)
        except asyncio.CancelledError:
            staggered.cancel()
            await asyncio.gather(staggered, *cancel(pending), return_exceptions=True)
            raise

        remove_failures_from(done)

        if done and return_when == asyncio.FIRST_COMPLETED:
            break

        logging.debug("%d discovery tasks are still running...", len(pending))

        if pending and return_when != asyncio.FIRST_COMPLETED:
            pending.update(done)
            done.clear()

    remove_failures_from(done)
    staggered.cancel()
    await asyncio.gather(staggered, *cancel(pending), return_exceptions=True)

    if done:
        logging.info("Discovered batteries: %s", {task.result() for task in done})
        if return_when == asyncio.FIRST_COMPLETED:
            return await next(iter(done))

        return {task.result() for task in done}

    raise DiscoveryError(
        "Unable to connect to the batterie at "
        f"host={host} port={port}, or your batterie is not supported yet.\n"
        "Please see https://github.com/markusbiggus/sonnen_api_v2/DiscoveryError\n"
        f"Failures={str(failures)}"
    )


class DiscoveryError(Exception):
    """Raised when unable to discover batterie"""
