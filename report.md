## Comparison among HTTP packages:
* httpx with global and non-global connection
* aiohttp
* requests.Session

## Results

### aiohttp time 2.93s on 5,000 consecutive requests.

### httpx global connection time 5.02s on consecutive 5,000 requests

### Request Session time 9.66s on consecutive 5,000 requests

### httpx no global connection time 32.13s on async (with [gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)) 5,000 requests
I don't know why httpx does not perform well with gather. Global connection also had the same
performance. It is very strange to be worse than global_connection.

* It may be related to local client-server test, and the response is small.
* It may be other reasons.

### httpx no global connection time 87.38s on consecutive 5,000 requests

### aiohttp [gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) time 8.17s on 1,000,000 requests!

## Conclusion

In terms of performance, **aiohttp** is the best option.

## Missing implementation

* requests with threads.
