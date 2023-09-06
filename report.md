## Comparison among HTTP packages:
* httpx with global and non-global connection
* aiohttp with "global" and "non-global" ClientSession
* requests.Session

## Results

### aiohttp global time 2.51s on 5,000 consecutive requests.

### aiohttp non-global time 2.78s on 5,000 consecutive requests.

### httpx global connection time 5.02s on consecutive 5,000 requests

### httpx non-global connection time 87.38s on consecutive 5,000 requests

### Request Session time 9.66s on consecutive 5,000 requests

### httpx no global connection time 32.13s on async (with [gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)) 5,000 requests
I don't know why httpx does not perform well with gather.

### aiohttp [gather](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) time 8.17s on 1,000,000 requests!

## Conclusion

In terms of performance, **aiohttp** is the best option.

## Missing implementation

* requests with threads.
