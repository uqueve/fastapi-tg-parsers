import asyncio
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError


@dataclass
class ReportBakuParser(BaseParser):
    request_object: BaseRequest
    headers: dict = None
    city: SiteModel = SiteModel.BAKU
    name: str = 'baku'
    __base_url = 'https://report.az'
    __news_url = __base_url + '/ru/news-feed/'
    referer = 'https://report.az/ru/'
    # TODO: 503 Service Temporarily Unavailable

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            json_obj = await self.request_object.get_json(url=url, json=True, session=self.session)

        if not json_obj.get('posts'):
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=json_obj)
        articles = json_obj['posts']
        for article in articles[:10]:
            link = self.__base_url + article['url']
            urls.append(link)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=json_obj)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', class_='news-title').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        main_div = soup.find('div', class_='editor-body')
        if main_div:
            ps = main_div.find_all('p')
            if ps:
                for p in ps:
                    content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []

        image = soup.find('div', class_='news-cover')
        if image:
            image = image.find('div', class_='image')
            if image:
                image = image.find('img').get('src')
                image_urls.append(image)
        return image_urls


async def test() -> None:
    parser = ReportBakuParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
