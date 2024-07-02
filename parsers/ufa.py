import asyncio
import contextlib
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    # 'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}


@dataclass
class UfaParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.UFA
    name: str = 'ufa'
    __base_url: str = 'https://prufy.ru'
    __news_url: str = 'https://prufy.ru/'
    referer: str = 'https://prufy.ru/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        main_block = soup.find('div', class_='news-list-news')
        if not main_block:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        items = main_block.find_all(
            'div',
            class_='lenta-item',
            limit=6,
        )
        if not items:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('http'):
                url = self.__base_url + url
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', attrs={'itemprop': 'headline'})
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        content = soup.find('div', attrs={'itemprop': 'articleBody'})
        if not content:
            return None
        ps = content.find_all('p')
        for p in ps:
            p = p.text
            if p:
                body += p.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        img_raw = soup.find('img', class_='detail_picture')
        if img_raw:
            img = img_raw.get('src')
            if img:
                if not img.startswith('http'):
                    img = self.__base_url + img
                if not img.endswith(('jpg', 'webp')):
                    with contextlib.suppress(IndexError):
                        img = img.split('?')[0]
                photos.append(img)
        return photos


async def test() -> None:
    parser = UfaParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
