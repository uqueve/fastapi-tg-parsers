import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from utils.models import Post


@dataclass
class BaseParser(ABC):

    max_news: int = 3

    @abstractmethod
    async def find_news_urls(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def find_title(self, *args) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def find_body(self, *args) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def find_photos(self, *args) -> list[str] | list:
        raise NotImplementedError

    def get_new(self, soup: BeautifulSoup | dict, url: str) -> Post | None:
        title = None
        try:
            title = self.find_title(soup)
        except AttributeError as ex:
            print(ex)

        if not title:
            return None

        body = None
        try:
            body = self.find_body(soup)
        except Exception as ex:
            print(ex)

        if not body:
            return None

        image_links = []
        try:
            image_links = self.find_photos(soup)
        except Exception as ex:
            print(ex)

        date = datetime.now()

        return Post(
            title=title,
            body=body,
            image_links=image_links,
            date=date,
            link=url,
        )

    @abstractmethod
    async def get_news(self, *args) -> list[Post]:
        raise NotImplementedError
