import asyncio
import random
from dataclasses import field, dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://kolyma.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


@dataclass
class MagadanParser(BaseParser, BaseRequest):
    name: str = 'magadan'
    __base_url: str = 'https://kolyma.ru'
    __news_url: str = 'https://kolyma.ru/index.php?do=cat&category=news'
    referer: str = 'https://kolyma.ru/index.php?do=cat&category=news'

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
        items = soup.find_all('div', class_='news-post article-post')
        for item in items:
            url_raw = item.find('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', attrs={'itemprop': 'headline name'})
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        content = soup.find('div', attrs={'itemprop': 'articleBody'})
        if not content:
            return None
        body += content.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        content_div = soup.find('div', class_='fullnews22')
        if content_div:
            photo_divs = content_div.find('img')
            if photo_divs:
                photos.append(self.__base_url + photo_divs.get('src'))
        return photos


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = MagadanParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())