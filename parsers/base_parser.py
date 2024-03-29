import datetime as dt
import logging
from typing import Any

import aiohttp
import requests
from aiohttp import ClientTimeout, ClientResponse

from utils.models import Post


class BaseParser:
    name = str()
    __base_url = str()
    __news_url = str()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    proxies = [
        {
            'http': 'http://EVBZEn:QwqX7v@46.3.147.105:8000',
        },
        {
            'http': 'http://oaF9Fm:Yj4Tr3@88.218.73.67:9886',
        },
        {
            'http': 'http://oaF9Fm:Yj4Tr3@88.218.75.9:9658',
        }
    ]

    def __init__(self):
        if self.__base_url not in self.__news_url:
            self.__news_url = self.__base_url + self.__news_url

    def get_new_news(self, last_news_date=None, max_news=100) -> [Post]:
        pass

    @staticmethod
    def check_is_new_news(last_news_date: dt.datetime, current_news_date: dt.datetime):
        return last_news_date is None or \
               dt.datetime.fromisoformat(str(current_news_date)) > dt.datetime.fromisoformat(str(last_news_date))

    def execute_parsing(self, last_news_date=None, max_news=100) -> [Post]:
        logging.info(f'\t- START {self.name} parser execution!')
        try:
            posts = self.get_new_news(last_news_date, max_news)
            posts = list(filter(lambda post: post.get_text() and post.get_title(), posts))[:max_news]

            for post in posts:
                post.parser_name = self.name

            # for p in posts:
            #     p.body += f'\n[{self.name}]'

            logging.info(f'\t- SUCCESSFUL {self.name} parser execution!')
            return posts
        except Exception as e:
            logging.error(f'\t- ERROR in {self.name} parser execution: {e}')
            return []
        finally:
            logging.info(f'\t- STOP {self.name} parser execution!')

    def _make_request(self, url, headers=None):
        if not headers:
            headers = self.headers
        try:
            return requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            logging.warning(
                f'\t\t- Warning! the standard request error in {self.name} parser: {e}, make proxie request.')
            return self.__make_request_with_proxies(url=url)

    async def _make_async_request(self, url, headers=None, json: bool = False) -> Any:
        if not headers:
            headers = self.headers
        try:
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

    def __make_request_with_proxies(self, url, headers=None):
        try:
            if not headers:
                headers = self.headers
            for proxie in self.proxies:
                try:
                    response = requests.get(url=url, headers=headers, proxies=proxie, timeout=30)
                    if response.status_code // 100 != 2:
                        logging.warning(
                            f'\t\t- Warning! the proxie request error in {self.name} parser. status code: {response.status_code}')
                        continue
                    return response
                except Exception as ee:
                    logging.warning(
                        f'\t\t- Warning! the proxie request error in {self.name} parser: {ee}')
                    continue
        except Exception as e:
            logging.error(f'\t\t- Error in {self.name} parser: {e}')
            return []
        return []

    async def __make_async_request_with_proxies(self, url, headers=None, json: bool = False) -> Any:
        try:
            if not headers:
                headers = self.headers
            for proxy_dict in self.proxies:
                try:
                    timeout = ClientTimeout(total=30)
                    proxy = proxy_dict.items().mapping['http']
                    async with aiohttp.request(method='GET', url=url, headers=headers, timeout=timeout, proxy=proxy) as response:
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
