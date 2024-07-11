import asyncio
import json
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'AMP-Same-Origin': 'true',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://ria.ru/amp/location_Omsk/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


@dataclass
class OmskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.OMSK
    name: str = 'omsk'
    __base_url = 'https://ria.ru'
    __news_url = __base_url + '/amp/location_Omsk/more.json'
    referer = 'https://ria.ru/amp/location_Omsk/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            json_obj = await self.request_object.get_json(url=url, session=self.session)

        if not json_obj.get('items'):
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=json_obj)
        for new in json_obj['items']:
            urls.append(new['url'])
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=json_obj)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find(['div', 'h1'], class_='article__title').text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        div = soup.find('div', class_='article__body js-mediator-article mia-analytics')
        divs = div.find_all('div', 'article__block')
        for p in divs:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError:
                continue
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        photo_div = soup.find('div', class_='article__announce')
        photo_div = photo_div.find('div', class_='photoview__open')
        if not photo_div:
            return image_urls
        data = [json.loads(script.text) for script in photo_div.find_all('script', type='application/ld+json')]

        if data:
            photo = data[-1]['url']
            image_urls.append(photo)
        return image_urls


async def test() -> None:
    parser = OmskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
