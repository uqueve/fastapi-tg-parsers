import datetime as dt
import logging
from typing import Any
from collections import OrderedDict
import aiohttp
import requests
from aiohttp import ClientTimeout, ClientResponse

from utils.models import Post


class BaseParser:
    name = str()
    __base_url = str()
    __news_url = str()

    headers = OrderedDict({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, zstd',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    })

    # proxies = [
    #     {
    #         'http': 'http://EVBZEn:QwqX7v@46.3.147.105:8000',
    #     },
    #     {
    #         'http': 'http://oaF9Fm:Yj4Tr3@88.218.73.67:9886',
    #     },
    #     {
    #         'http': 'http://oaF9Fm:Yj4Tr3@88.218.75.9:9658',
    #     }
    # ]

    proxies = [
        {
            'url': 'http://46.3.147.105:8000',
            'login': 'EVBZEn',
            'pass': 'QwqX7v'
        },
        {
            'url': 'http://88.218.73.67:9886',
            'login': 'oaF9Fm',
            'pass': 'Yj4Tr3'
        },
        {
            'url': 'http://88.218.75.9:9658',
            'login': 'oaF9Fm',
            'pass': 'Yj4Tr3'
        }
    ]

    def __init__(self):
        if self.__base_url not in self.__news_url:
            self.__news_url = self.__base_url + self.__news_url

    def get_new_news(self, last_news_date=None, max_news=100) -> [Post]:
        pass

    async def _make_async_request(self, url, headers=None, json: bool = False, referer: str = None) -> Any:
        if not headers:
            headers = self.headers
            if referer:
                headers['referer'] = referer
        try:
            # answers = socket.getaddrinfo('grimaldis.myguestaccount.com', 443)
            # (family, type, proto, canonname, (address, port)) = answers[0]
            timeout = ClientTimeout(total=5)
            async with aiohttp.request(method='GET', url=url, headers=headers, timeout=timeout) as response:
                if response.status != 200:
                    logging.warning(f'### {response.status} - {url}. {await response.text()}')
                    logging.info('Trying request with proxies')
                    return await self.__make_async_request_with_proxies(url=url, json=json)
                if not json:
                    return await response.text()
                else:
                    return await response.json()
        except Exception as e:
            logging.warning(
                f'\t\t- Warning! the standard request error in {self.name} parser: {e}, make proxie request.')
            return await self.__make_async_request_with_proxies(url=url)

    async def __make_async_request_with_proxies(self, url, headers=None, json: bool = False) -> Any:
        # TODO: aiohttp/connector.py:909: RuntimeWarning: An HTTPS request is being sent through an HTTPS proxy.
        #  This support for TLS in TLS is known to be disabled in the stdlib asyncio (Python <3.11).
        #  This is why you'll probably see an error in the log below.
        #  It is possible to enable it via monkeypatching. For more details, see:
        #  https://bugs.python.org/issue37179
        #  https://github.com/python/cpython/pull/28073
        #  You can temporarily patch this as follows:
        #  https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support
        #  https://github.com/aio-libs/aiohttp/discussions/6044
        try:
            if not headers:
                headers = self.headers
            for proxy_dict in self.proxies:
                try:
                    timeout = ClientTimeout(total=30)
                    # proxy = proxy_dict.items().mapping['http']
                    proxy_url = proxy_dict['url']
                    proxy_login = proxy_dict['login']
                    proxy_pass = proxy_dict['pass']
                    auth = aiohttp.BasicAuth(login=proxy_login, password=proxy_pass)
                    async with aiohttp.request(method='GET',
                                               url=url,
                                               headers=headers,
                                               timeout=timeout,
                                               proxy=proxy_url,
                                               proxy_auth=auth) as response:
                        if response.status // 100 != 2:
                            logging.warning(
                                f'\t\t- Warning! the proxie request error in {self.name} parser. status code: {response.status}')
                            continue
                        if json:
                            return await response.json()
                        return await response.text()
                except Exception as ee:
                    logging.warning(
                        f'\t\t- Warning! the proxie request error in {self.name} parser: {ee}')
                    continue
        except Exception as e:
            logging.error(f'\t\t- Error in {self.name} parser: {e}')
            return []
        return []
