"""Simulate many consecutive requests to a URL with different HTTP request modules."""
from asyncio import run, gather, ensure_future
from aiohttp import ClientSession
from httpx import AsyncClient, Limits
from time import perf_counter
from requests import Session

URL = "http://0.0.0.0:9001"
N_REQUESTS = 5000

limits = Limits(max_connections=N_REQUESTS)

global_connection: AsyncClient | None = None


async def main() -> None:
    # await httpx_global_connection_test()
    # await httpx_no_global_connection_test()
    # await aiohttp_session_test()
    # await aiohttp_no_session_test()

    await httpx_no_global_connection_gather_test()
    # await aiohttp_gather()

    await _close_httpx_connection()


async def httpx_global_connection_test() -> None:
    """Global AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        client = _get_httpx_connection()
        responses.append(await client.get(URL))

    print(f"httpx global connection time {perf_counter()-start:.2f}s on {len(responses)} requests")


async def httpx_no_global_connection_test() -> None:
    """Creating always a new AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        async with AsyncClient() as client:
            responses.append(await client.get(URL))

    print(f"httpx no global connection time {perf_counter()-start:.2f}s on {len(responses)} requests")


async def httpx_no_global_connection_gather_test() -> None:
    start = perf_counter()
    async with AsyncClient(limits=limits) as client:
        requests = [client.get(URL) for _ in range(N_REQUESTS)]
        responses = await gather(*requests)

    print(f"httpx no global connection gather time {perf_counter()-start:.2f}s on {len(responses)} requests")


async def aiohttp_session_test() -> None:
    start = perf_counter()
    responses = []
    async with ClientSession() as session:
        for _ in range(N_REQUESTS):
            async with session.get(URL) as response:
                responses.append(await response.text())

    print(f"aiohttp session time {perf_counter() - start:.2f}s on {len(responses)} requests")


async def aiohttp_no_session_test() -> None:
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        async with ClientSession() as session:
            async with session.get(URL) as response:
                responses.append(await response.text())

    print(f"aiohttp no session time {perf_counter() - start:.2f}s on {len(responses)} requests")


async def aiohttp_gather() -> None:
    start = perf_counter()
    async with ClientSession() as session:
        async with session.get(URL) as response:
            request_texts = [response.text() for _ in range(1_000_000)]  # Big number of requests.
            responses = await gather(*request_texts)

    print(f"aiohttp gather time {perf_counter() - start:.2f}s on {len(responses)} requests")


def request_session_test() -> None:
    session = Session()
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        responses.append(session.get(URL))

    print(f"Request Session time {perf_counter() - start:.2f}s on {len(responses)} requests")


def _get_httpx_connection() -> AsyncClient:
    global global_connection
    if global_connection is None:
        global_connection = AsyncClient(limits=limits)
        return global_connection

    return global_connection


async def _close_httpx_connection() -> None:
    global global_connection
    if global_connection is not None:
        await global_connection.aclose()
        global_connection = None

    return global_connection


if __name__ == "__main__":
    run(main())
    # request_session_test()
