import asyncio
import json
from urllib import request, parse

import aiohttp
from aiohttp import ClientTimeout

# link = 'http://45.142.215.106:1111/news'
# body = {'ids': ['66015f9a4b6a26f5d3d12093']}
# # body = parse.urlencode(body).encode()
# body = json.dumps(body).encode()
# req = request.Request(link, method='POST')
# req.add_header('Content-Type', 'application/json')
# resp = request.urlopen(req, data=body)
# print(resp.read())


async def start():
    timeout = ClientTimeout(total=5)
    url = 'http://45.142.215.106:1111/news'
    body = {'ids': ['66015f9a4b6a26f5d3d12093']}
    async with aiohttp.request(method='POST', url=url, timeout=timeout, json=body) as response:
        print(await response.json())


def main():
    asyncio.run(start())


main()