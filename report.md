## Comparison among HTTP packages:
* httpx with global and non-global connection
* requests.Session
* aiohttp

## Results

### aiohttp time 2.93s on 5,000 requests

### httpx global_connection time 5.02s on 5,000 requests

### Request Session time 9.66s on 5,000 requests

### httpx no_global_connection gather time 32.13s on 5,000 requests
I don't know why httpx does not perform well with gather. Global connection also had the same
performance. It is very strange to be worse than global_connection.

* It may be related to local client-server test, and the response is small.
* It may be other reasons.

### httpx no_global_connection time 87.38s on 5,000 requests

### aiohttp gather time 8.17s on 1,000,000 requests!!

## Conclusion

In terms of performance, **aiohttp** is the best option.

## Missing implementation

* requests with threads.
