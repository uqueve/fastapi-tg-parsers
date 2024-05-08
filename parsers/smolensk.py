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
    'if-modified-since': 'Fri, 26 Apr 2024 13:59:59 GMT',
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
class SmolenskParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.SMOLENSK
    name: str = 'smolensk'
    __base_url: str = 'https://smolensk-i.ru'
    __news_url: str = 'https://smolensk-i.ru/'
    referer: str = 'https://smolensk-i.ru/'

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
        soup = await self.get_soup(url=url, headers=headers)
        div = soup.find('div', class_='chronicle-posts')
        items = div.find_all('article', class_=lambda value: find_value(value, 'post-'))
        for item in items:
            url_raw = item.find('div', class_='entry-title').find('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', class_='entry-title')
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        body = ''
        content = soup.find('div', class_='entry-content')
        ps = content.find_all('p')
        for p in ps:
            if find_value(p.text, 'текст:'):
                continue
            body += p.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        content_div = soup.find('div', class_='entry-content')
        photo_divs = content_div.find_all(
            'figure',
            class_=lambda value: find_value(value, 'wp-block-image'),
        )
        for photo_div in photo_divs:
            if photo_div:
                photo = photo_div.find('img').get('src')
                photos.append(photo)
        return photos


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = SmolenskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
