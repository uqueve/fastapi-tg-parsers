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
class SurgutParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.SURGUT
    name: str = 'surgut'
    __base_url: str = 'https://sitv.ru'
    __news_url: str = 'https://sitv.ru/arhiv/news/'

    async def get_news(self, urls: list, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        async with self.session:
            for new_url in urls:
                if len(news) >= self.max_news:
                    return news
                soup = await self.get_soup(session=self.session, url=new_url)
                new = self.get_new(soup, url=new_url)
                if not new:
                    continue
                await asyncio.sleep(random.choice(range(5)))
                news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.create_session()
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, session=self.session)
        items = soup.find_all('div', class_='m3col elems')
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('a')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('h1', attrs={'itemprop': 'headline'}).text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        content = soup.find('div', attrs={'itemprop': 'articleBody'})
        return content.text.replace('\xa0', ' ').strip()

    def find_photos(self, soup: BeautifulSoup) -> list:
        return []


async def test() -> None:
    parser = SurgutParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
