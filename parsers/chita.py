import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup
from datetime import datetime, timezone

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


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
class ChitaParser(BaseParser, BaseRequest):
    name = 'chita'
    __base_url = 'https://www.mkchita.ru'
    __news_url = __base_url + '/news/'
    referer = 'https://www.mkchita.ru/'

    async def get_news(self, urls) -> list[Post]:
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

    async def find_news_urls(self, max_news=3) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        today_news_block = soup.find('ul', class_='news-listing__day-list')
        news = today_news_block.find_all('a', class_='news-listing__item-link')

        for new in news:
            url = new.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup) -> str | None:
        main_block = soup.find('main', class_='article')

        if not main_block:
            return None

        title = main_block.find('h1', class_='article__title').text.strip()

        return title

    def find_body(self, soup) -> str | None:
        content = ""

        main_block = soup.find('main', class_='article')
        contents_div = main_block.find('div', class_='article__body')
        contents = contents_div.find_all('p')
        for con in contents:
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []
        main_block = soup.find('main', class_='article')
        photo_div = main_block.find('img', class_='article__picture-image')

        if photo_div:
            photo = photo_div.get('src')
            image_urls.append(photo)
        return image_urls


async def test():
    parser = ChitaParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
