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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://crimea.ria.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    # 'sec-gpc': '1',
}


@dataclass
class KrimParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.KRIM
    name: str = 'krim'
    __base_url: str = 'https://crimea.ria.ru'
    __news_url: str = 'https://crimea.ria.ru/lenta/'
    referer: str = 'https://crimea.ria.ru/lenta/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        items = soup.find_all(
            'div',
            class_='list-item',
            limit=5,
        )
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find('a', attrs={'itemprop': 'url'})
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('http'):
                url = self.__base_url + url
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('div', class_='article__title')
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        content = soup.find(
            'div',
            class_=lambda v: find_value(v, 'article__body'),
        )
        if not content:
            return None
        ps = content.find_all('div', attrs={'class': 'article__block', 'data-type': ['text', 'quote']})
        for p in ps:
            p = p.text
            if p.startswith('Читайте также'):
                return body
            if p.endswith('РИА Новости Крым'):
                continue
            body += p.replace('\xa0', ' ').strip()
            body += '\n'
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        content_div = soup.find('div', class_='article__announce')
        if content_div:
            photo_divs = content_div.find('img')
            if photo_divs:
                photos.append(photo_divs.get('src'))
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = KrimParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
