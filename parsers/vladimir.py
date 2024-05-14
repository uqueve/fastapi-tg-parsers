import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError
from utils.models import Post, SiteModel

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


@dataclass
class VladimirParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.VLADIMIR
    name: str = 'vladimir'
    __base_url = 'https://progorod33.ru'
    __news_url = 'https://progorod33.ru/news'
    referer = 'https://progorod33.ru/news'

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
            await asyncio.sleep(random.randrange(8, 15))
            news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        news = soup.find_all(
            'article',
            class_=lambda value: find_value(value, 'news-line_news__'),
        )
        if not news:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for new in news:
            url = new.find('a')
            if url:
                url = self.__base_url + url.get('href')
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', attrs={'itemprop': 'headline'})
        if not title:
            return None
        title = title.text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''

        main_block = soup.find('div', attrs={'itemprop': 'articleBody'})
        if not main_block:
            return None
        contents = main_block.find_all('p')
        for con in contents:
            if not con:
                continue
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        image_raw = soup.find(
            'img',
            class_=lambda value: find_value(value, 'article-body_articleBodyImg'),
        )

        if image_raw:
            photo = self.__base_url + image_raw.get('src')
            image_urls.append(photo)
        return image_urls


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = VladimirParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
