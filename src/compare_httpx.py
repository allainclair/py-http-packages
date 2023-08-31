"""Simulate many consecutive requests to a URL with different HTTP request modules."""
from asyncio import run
from aiohttp import ClientSession
from httpx import AsyncClient
from time import perf_counter
from requests import Session

URL = "http://0.0.0.0:9001"
N_REQUESTS = 5000

global_connection: AsyncClient | None = None


async def global_connection_test() -> None:
    """Global AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        client = _get_global_connection()
        responses.append(await client.get(URL))

    print(f"httpx global_connection time {perf_counter()-start:.2f}s on {len(responses)} requests")


async def no_global_connection_test() -> None:
    """Creating always a new AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        async with AsyncClient() as client:
            responses.append(await client.get(URL))

    print(f"httpx no_global_connection time {perf_counter()-start:.2f}s on {len(responses)} requests")


async def aiohttp_() -> None:
    start = perf_counter()
    responses = []
    async with ClientSession() as session:
        for _ in range(N_REQUESTS):
            async with session.get(URL) as response:
                responses.append(await response.text())

    print(f"aiohttp time {perf_counter() - start:.2f}s on {len(responses)} requests")


def request_session_test() -> None:
    session = Session()
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        responses.append(session.get(URL))

    print(f"Request Session time {perf_counter() - start:.2f}s on {len(responses)} requests")


async def main() -> None:
    await global_connection_test()
    await no_global_connection_test()
    await _close_global_connection()
    await aiohttp_()


def _get_global_connection() -> AsyncClient:
    global global_connection
    if global_connection is None:
        global_connection = AsyncClient()
        return global_connection

    return global_connection


async def _close_global_connection() -> AsyncClient:
    global global_connection
    if global_connection is not None:
        await global_connection.aclose()

    return global_connection


if __name__ == "__main__":
    run(main())
    request_session_test()
