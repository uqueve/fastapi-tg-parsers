import asyncio
import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest

logger = logging.getLogger(__name__)


@dataclass
class BaseParser(ABC):
    city: SiteModel | None = None
    name: str | None = None
    max_news: int = 3
    title: str | None = None
    body: str | None = None
    image_links: list[str] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)
    session: ClientSession = None
    request_object: BaseRequest = None
    referer: str = None
    headers: dict = None

    @abstractmethod
    async def find_news_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def find_title(self, soup: BeautifulSoup | dict) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def find_body(self, soup: BeautifulSoup | dict) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def find_photos(self, soup: BeautifulSoup | dict) -> list[str] | list:
        raise NotImplementedError

    def get_new(self, soup: BeautifulSoup | dict, url: str) -> Post | None:
        try:
            self.title = self.find_title(soup)
        except Exception:
            logger.exception(f'TITLE ERROR. Парсер: {self.name}. URL: {url}')

        if not self.title:
            return None

        try:
            self.body = self.find_body(soup)
        except Exception:
            logger.exception(f'BODY ERROR. Парсер: {self.name}. URL: {url}')

        if not self.body:
            return None

        try:
            self.image_links = self.find_photos(soup)
        except Exception:
            logger.exception(f'IMAGE LINKS ERROR. Парсер: {self.name}. URL: {url}')

        return Post(
            title=self.title,
            body=self.body,
            image_links=self.image_links,
            date=self.date,
            link=url,
            parser_name=str(self.city),
        )

    @abstractmethod
    async def get_news(self, urls: list, max_news: int | None = 3, headers: dict = None, json: bool = False) -> list[Post]:
        raise NotImplementedError

    async def _get_news(self, urls: list, max_news: int | None = 3, headers: dict = None, json: bool = False) -> list[Post]:
        if not self.headers:
            headers = self.request_object.get_base_headers()
        self.session: ClientSession = self.request_object.create_session(headers=headers)
        if max_news:
            self.max_news = max_news
        news = []
        try:
            async with self.session:
                for new_url in urls:
                    if len(news) >= self.max_news:
                        return news
                    if json:
                        soup = await self.request_object.get_json(
                            session=self.session,
                            url=new_url,
                            headers=headers,
                            referer=self.referer)
                    else:
                        soup = await self.request_object.get_soup(
                            session=self.session,
                            url=new_url,
                            headers=headers,
                            referer=self.referer)
                    new = self.get_new(soup, url=new_url)
                    if not new:
                        continue
                    await asyncio.sleep(random.randrange(8, 15))
                    news.append(new)
        finally:
            await self.session.close()
        return news

    @staticmethod
    def base_find_value(value: str, example: str) -> bool:
        if value:
            if value.startswith(example):
                return True
            return False
        return False
