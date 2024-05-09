import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post, SiteModel


@dataclass
class BryanskParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.BRYANSK
    name: str = 'bryansk'
    __base_url: str = 'https://newsbryansk.ru/'
    __news_url: str = 'https://newsbryansk.ru/'

    async def get_news(self, urls: list, max_news: int | None = None) -> list[Post]:
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
        items = soup.find_all(
            'div',
            class_=lambda value: find_value(value, 'big-news-list-item big-news-list-'),
        )
        for item in items:
            url_raw = item.find_next('h2').find('a')
            if not url_raw:
                continue
            url = self.__base_url + url_raw.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('div', class_='detale-news-block__pin').find('h1').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        content = soup.find('span', attrs={'itemprop': 'articleBody'})
        return content.text.replace('\xa0', ' ').strip()

    def find_photos(self, soup: BeautifulSoup) -> list:
        photo_raw = soup.find('div', 'detale-news-block__image')
        if photo_raw:
            photo = photo_raw.find('img').get('src')
            return [photo]
        return []


def find_value(value: str, example: str) -> bool:
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test() -> None:
    parser = BryanskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
