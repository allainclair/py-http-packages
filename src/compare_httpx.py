from asyncio import run, gather
from sys import argv
from httpx import AsyncClient
from time import perf_counter

URL = "http://0.0.0.0:9001"
N_REQUESTS = 10_000

global_connection: AsyncClient | None = None


async def global_connection_test() -> None:
    """Simulate consecutive N_REQUESTS to the URL with a global AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        client = _get_global_connection()
        responses.append(await client.get(URL))

    print(f"global_connection time {perf_counter()-start}s for {len(responses)} requests")


async def no_global_connection_test() -> None:
    """Simulate consecutive N_REQUESTS to the URL creating a new AsyncClient."""
    start = perf_counter()
    responses = []
    for _ in range(N_REQUESTS):
        async with AsyncClient() as client:
            responses.append(await client.get(URL))

    print(f"no_global_connection time {perf_counter()-start}s for {len(responses)} requests")


async def main() -> None:
    await global_connection_test()
    await no_global_connection_test()
    await _close_global_connection()


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
