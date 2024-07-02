import asyncio
from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError


@dataclass
class KrasnodarParser(BaseParser):
    request_object: BaseRequest
    headers: dict = None
    city: SiteModel = SiteModel.KRASNODAR
    name: str = 'krasnodar'
    __base_url: str = 'https://kubnews.ru'
    __news_url: str = 'https://kubnews.ru/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        div = soup.find('div', class_='band band_main')
        items = div.find_all('div', class_='band__item')
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('a', class_='band__link')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('h1', class_='material__name').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        content = soup.find(
            'div',
            class_=lambda value: find_value(value, 'material__content_detail_text'),
        )
        return content.text.replace('\xa0', ' ').strip()

    def find_photos(self, soup: BeautifulSoup) -> list:
        photo = self.__base_url + soup.find('figure', class_='figure').find('a').get(
            'href',
        )
        return [photo]


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = KrasnodarParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
