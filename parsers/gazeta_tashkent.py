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
class TashkentParser(BaseParser):
    request_object: BaseRequest
    headers: dict = None
    city: SiteModel = SiteModel.TASHKENT
    name: str = 'tashkent'
    __base_url = 'https://www.gazeta.uz/'
    __news_url = __base_url + 'ru/'
    referer = 'https://www.gazeta.uz/ru/'

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
        articles_block = soup.find('div', class_='newsblock-2')
        articles = articles_block.find_all('div', class_='nblock', limit=10)
        if not articles:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for article in articles:
            link = 'https://www.gazeta.uz' + article.find_next('a').get('href')
            urls.append(link)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', attrs={'id': 'article_title'}).text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''

        main_div = soup.find('div', attrs={'itemprop': 'articleBody'})
        ps = main_div.find_all('p')
        for p in ps:
            content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []

        images = soup.find_all('a', class_='lightbox-img')
        if images:
            for image in images:
                image_urls.append(image.get('href'))
        return image_urls


async def test() -> None:
    parser = TashkentParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
