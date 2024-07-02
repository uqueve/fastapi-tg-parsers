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
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


@dataclass
class IrkutskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.IRKUTSK
    name: str = 'irkutsk'
    __base_url: str = 'https://www.irk.ru'
    __news_url: str = 'https://www.irk.ru/news/'
    referer: str = 'https://www.irk.ru/news/'

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
            'li',
            class_=lambda v: find_value(v, 'b-news-article-list-item'),
            limit=15,
        )
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find('a')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', class_='lenta-article__title')
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        content = soup.find(
            'div',
            class_='lenta-article__text j-material-text j-copyright-insert',
        )
        if not content:
            return None
        ps = content.find_all('p')
        for p in ps:
            body += p.text.replace('\xa0', ' ').strip()
            body += '\n'
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        content_div = soup.find('figure', class_='lenta-article__figure')
        if content_div:
            photo_divs = content_div.find('a')
            if photo_divs:
                photos.append(photo_divs.get('href'))
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = IrkutskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
