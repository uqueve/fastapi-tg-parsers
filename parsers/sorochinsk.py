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
class SorochinskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = None
    city: SiteModel = SiteModel.SOROCHINSK
    name: str = 'sorochinsk'
    __base_url: str = 'https://orenday.ru'
    __news_url: str = 'https://orenday.ru/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        items = soup.find_all('a', class_='new-title font-bold font-times')
        if not items:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url = self.__news_url + item.get('href')
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = (
            soup.find(
                'h1',
                class_=lambda value: find_value(value, 'main-new-title text'),
            )
            .text.replace('\xa0', ' ')
            .strip()
        )
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        body = ''
        content = soup.find('div', class_='mt-[19px] mb-[10px]')
        if content:
            body += content.text.replace('\xa0', ' ').strip()
        main_content = soup.find('div', class_='content')
        if main_content:
            body += main_content.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        div_photo = soup.find('img', attrs={'rel': 'image_src'})
        if div_photo:
            photo = self.__news_url + div_photo.get('src')
            if not photo.startswith('https:'):
                photo = self.__base_url + photo
            return [photo]
        else:
            div_photo = soup.find('div', attrs={'itemprop': 'articleBody'})
            if div_photo:
                photo_raw = div_photo.find('img')
                if photo_raw:
                    photo = photo_raw.get('src')
                    if not photo.startswith('https:'):
                        photo = self.__base_url + photo
                    return [photo]
        return []


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = SorochinskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
