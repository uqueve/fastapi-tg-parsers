import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from utils.models import Post


@dataclass
class BaseParser(ABC):

    max_news: int = 3
    title: str | None = None
    body: str | None = None
    image_links: list[str] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)

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
        except AttributeError as ex:
            print(ex)

        if not self.title:
            return None

        try:
            self.body = self.find_body(soup)
        except Exception as ex:
            print(ex)

        if not self.body:
            return None

        try:
            self.image_links = self.find_photos(soup)
        except Exception as ex:
            print(ex)

        return Post(
            title=self.title,
            body=self.body,
            image_links=self.image_links,
            date=self.date,
            link=url,
        )

    @abstractmethod
    async def get_news(self, urls: list[str], max_news: int = 3) -> list[Post]:
        raise NotImplementedError