import asyncio
import random
import re
from dataclasses import dataclass

from bs4 import BeautifulSoup
from datetime import datetime, timezone

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
class CherepovecParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.CHEREPOVEC
    name: str = 'cherepovec'
    __base_url = 'https://cherinfo.ru'
    __news_url = __base_url + '/news'
    referer = 'https://cherinfo.ru/news'

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
            await asyncio.sleep(random.randrange(8, 15))
            news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        main_articles = soup.find('div', class_='container content wrapper')
        articles_block = main_articles.find_all('a', class_='lenta-title', limit=self.max_news)

        for article in articles_block:
            try:
                link = article.get('href')
                urls.append(link)
            except Exception as ex:
                print(ex)
                continue
        return urls

    def find_title(self, soup) -> str | None:
        main_block = soup.find('div', class_='col-lg-9 col-md-9 col-sm-12 col-xs-12 sticky-main print-wide ny-2023')
        if not main_block:
            return
        title = main_block.find('h1', class_='margin-bottom-small').text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ""
        main_block = soup.find('div', class_='col-lg-9 col-md-9 col-sm-12 col-xs-12 sticky-main print-wide ny-2023')
        contents_div = main_block.find('div', class_='js-mediator-article article-text')
        contents = contents_div.find_all('p')
        for con in contents:
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = set()
        main_block = soup.find('div', class_='col-lg-9 col-md-9 col-sm-12 col-xs-12 sticky-main print-wide ny-2023')
        contents_div = main_block.find('div', class_='js-mediator-article article-text')
        contents = contents_div.find_all('p')
        for con in contents:
            photo = con.find('img')
            if photo:
                if photo := photo.get('src'):
                    image_urls.add(photo)

        photo_div = main_block.find('div', class_='widget print-hidden')

        if photo_div:
            photos = photo_div.find_all('a')
            for photo in photos:
                if photo := photo.get('href'):
                    image_urls.add(photo)

        return list(image_urls)


async def test():
    parser = CherepovecParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
