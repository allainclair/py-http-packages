## Comparison among HTTP packages:
* httpx with global and non-global connection
* requests.Session
* aiohttp

## Results

aiohttp time 2.93s on 5000 requests

httpx global_connection time 5.02s on 5000 requests

Request Session time 9.66s on 5000 requests

httpx no_global_connection time 87.38s on 5000 requests
