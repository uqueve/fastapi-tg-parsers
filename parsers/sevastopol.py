import asyncio
import random
from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError
from parsers.models.cities import SiteModel
from parsers.models.posts import Post

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
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


@dataclass
class SevastopolParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.SEVASTOPOL
    name: str = 'sevastopol'
    __base_url: str = 'https://sevastopol.su'
    __news_url: str = 'https://sevastopol.su/'
    referer: str = 'https://sevastopol.su/'

    async def get_news(self, urls: list, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        async with self.session:
            for new_url in urls:
                if len(news) >= self.max_news:
                    return news
                soup = await self.get_soup(session=self.session, url=new_url, headers=headers, referer=self.referer)
                new = self.get_new(soup, url=new_url)
                await asyncio.sleep(random.randrange(8, 15))
                if not new:
                    continue
                news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.create_session(headers=headers)
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers, session=self.session)
        items = soup.find_all('div', class_=lambda v: find_value(v, 'views-row flex mobile-center'), limit=15)
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('https:'):
                url = self.__base_url + url
            if url:
                urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('span', attrs={'itemprop': 'headline'})
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        main_div = soup.find('div', class_='block-basic-content')
        ps = main_div.find_all('p')
        for p in ps:
            if not p.text:
                continue
            body += p.text.replace('\xa0', ' ').strip() + '\n'
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []

        main_photo = soup.find('div', class_='news__anouncement-image')
        if main_photo and (photo_raw := main_photo.find('img')):
            if photo_raw:
                photos.append(self.__base_url + photo_raw.get('src'))

        main_div = soup.find('div', class_='block-basic-content')
        body_div = main_div.find(
            'div',
            attrs={'itemprop': 'text'},
        )
        photo_divs = body_div.find_all('img')
        for photo_div in photo_divs:
            photo = self.__base_url + photo_div.get('src')
            photos.append(photo)
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = SevastopolParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
