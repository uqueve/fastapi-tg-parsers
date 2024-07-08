import asyncio
import random
from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError


@dataclass
class BryanskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = None
    city: SiteModel = SiteModel.BRYANSK
    name: str = 'bryansk'
    __base_url: str = 'https://newsbryansk.ru/'
    __news_url: str = 'https://newsbryansk.ru/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url
        try:
            async with self.session:
                soup = await self.request_object.get_soup(url=url, session=self.session)
        finally:
            await self.session.close()
        items = soup.find_all(
            'div',
            class_=lambda value: find_value(value, 'big-news-list-item big-news-list-'),
        )
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('h2').find('a')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('div', class_='detale-news-block__pin').find('h1').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        content = soup.find('span', attrs={'itemprop': 'articleBody'})
        return content.text.replace('\xa0', ' ').strip()

    def find_photos(self, soup: BeautifulSoup) -> list:
        photo_raw = soup.find('div', 'detale-news-block__image')
        if photo_raw:
            photo = photo_raw.find('img').get('src')
            return [photo]
        return []


def find_value(value: str, example: str) -> bool:
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test() -> None:
    parser = BryanskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
