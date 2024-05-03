import asyncio
import json
import random
from dataclasses import field, dataclass
from datetime import datetime

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


headers = {
    'AMP-Same-Origin': 'true',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://ria.ru/amp/location_Vladivostok/',
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
class VladivostokParser(BaseParser, BaseRequest):
    name: str = 'tumen'
    __base_url: str = 'https://ria.ru'
    __news_url: str = 'https://ria.ru/amp/location_Vladivostok/more.json'
    referer: str = 'https://ria.ru/amp/location_Vladivostok/'

    async def get_news(self, urls, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url, headers=headers, referer=self.referer)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.randrange(3, 8))
            news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        json_obj = await self.get_json(url=url, headers=headers)
        for new in json_obj['items']:
            urls.append(new['url'])
        return urls

    def find_title(self, soup) -> str | None:
        title = soup.find(['div', 'h1'], class_='article__title').text.strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ""
        div = soup.find('div', class_='article__body js-mediator-article mia-analytics')
        divs = div.find_all('div', 'article__block')
        for p in divs:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError as ex:
                continue
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []
        photo_div = soup.find('div', class_='article__announce')
        photo_div = photo_div.find('div', class_='photoview__open')
        data = [json.loads(script.text) for script in photo_div.find_all('script', type='application/ld+json')]

        # TODO: WEBP > JPG ?
        if data:
            photo = data[-1]['url']
            image_urls.append(photo)
        return image_urls


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = VladivostokParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())