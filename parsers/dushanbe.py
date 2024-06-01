import asyncio
import random
from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}


@dataclass
class DushanbeParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.DUSHANBE
    name: str = 'dushanbe'
    __base_url: str = 'https://tj.sputniknews.ru'
    __news_url: str = 'https://tj.sputniknews.ru/country/'
    referer: str = 'https://tj.sputniknews.ru/country/'

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
                if not new:
                    continue
                await asyncio.sleep(random.randrange(8, 15))
                news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.create_session(headers=headers)
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers, session=self.session)
        items = soup.find_all('div', class_=lambda v: find_value(v, 'list__item'), limit=4)
        if not items:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('a', class_='list__title')
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('https:'):
                url = self.__base_url + url
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('div', attrs={'itemprop': 'headline'})
        if not title:
            print('no title')
            return None
        title = title.text.replace('\xa0', ' ').strip()
        print(title)
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        main_body = soup.find('div', attrs={'itemprop': 'articleBody'})
        if not main_body:
            return None
        splited_body = main_body.text.split('.')
        for part in splited_body:
            if '&gt;&gt' in part or 'Подписывайтесь' in part or 'Sputnik' in part:
                continue
            body += part + '.'
        body = body.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        main_div = soup.find('div', attrs={'itemprop': 'associatedMedia'})
        if main_div:
            photo = main_div.text
            photos.append(photo)
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test() -> None:
    parser = DushanbeParser()
    urls = await parser.find_news_urls()
    print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
