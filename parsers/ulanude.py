import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post, SiteModel

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class UlanUdeParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.ULANUDE
    name: str = 'ulanude'
    __base_url = 'https://m.baikal-daily.ru'
    __news_url = __base_url
    referer = 'https://m.baikal-daily.ru/'

    async def get_news(self, urls: list, max_news: int | None = None) -> list[Post]:
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
        soup = await self.get_soup(url=url, headers=headers)
        news = soup.find_all(
            'div',
            class_=lambda value: value.startswith('news-item news-item') if value else False,
        )
        # second way to find tags, a more simple to understand
        # news = soup.find_all('div', class_=lambda value: find_value(value))

        for new in news:
            url = self.__base_url + new.find_next('a').get('href')
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        main_block = soup.find('article', class_='news-detail')
        if not main_block:
            return None
        title = main_block.find('h1').text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        main_block = soup.find('article', class_='news-detail')
        content_div = main_block.find('div', class_='news-text')

        if not content_div:
            return None

        content += content_div.text.replace('\xa0', ' ').replace('\r\n', '').strip()
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        main_block = soup.find('article', class_='news-detail')
        photo_div = main_block.find('img', class_='preview_picture')

        if photo_div:
            photo = self.__base_url + photo_div.get('src')
            image_urls.append(photo)
        return image_urls


def find_value(value: str) -> bool:
    if value:
        return bool(value.startswith('news-item news-item'))
    return False


async def test() -> None:
    parser = UlanUdeParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
