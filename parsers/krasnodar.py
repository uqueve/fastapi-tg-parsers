import asyncio
import random
from dataclasses import field, dataclass
from datetime import datetime

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


@dataclass
class KrasnodarParser(BaseParser, BaseRequest):
    name: str = 'krasnodar'
    __base_url: str = 'https://kubnews.ru'
    __news_url: str = 'https://kubnews.ru/'

    async def get_news(self, urls, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.choice(range(5)))
            news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url)
        div = soup.find('div', class_='band band_main')
        items = div.find_all('div', class_='band__item')
        for item in items:
            url_raw = item.find_next('a', class_='band__link')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('h1', class_='material__name').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        content = soup.find('div', class_=lambda value: find_value(value, 'material__content_detail_text'))
        return content.text.replace('\xa0', ' ').strip()

    def find_photos(self, soup: BeautifulSoup) -> list:
        photo = self.__base_url + soup.find('figure', class_='figure').find('a').get('href')
        return [photo]


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = KrasnodarParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
