import asyncio
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
    'application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class NovokuznetskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.NOVOKUZNETSK
    name: str = 'novokuznetsk'
    __base_url = 'https://novokuznetsk.su'
    __news_url = __base_url
    referer = 'https://novokuznetsk.su/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        div = soup.find('div', class_='grid grid-cols-1 md:grid-cols-2 gap-6')
        if not div:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        news = div.find_all('a')
        if not news:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for new in news:
            url = self.__base_url + new.get('href')
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        main_block = soup.find('div', class_='text-2sm')
        if not main_block:
            return None
        title = main_block.find('h1').text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        main_block = soup.find('div', class_='text-2sm')
        contents = main_block.find_all('p')
        for con in contents:
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        main_block = soup.find('div', class_='text-2sm')
        photo_div = main_block.find('img')

        if photo_div:
            photo = photo_div.get('src')
            image_urls.append(photo)
        return image_urls


async def test() -> None:
    parser = NovokuznetskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
