import asyncio
import random
from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError
from utils.models import Post, SiteModel

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://24.kz/ru/news/social/itemlist/tag/%D0%A0%D0%B8%D0%B4%D0%B4%D0%B5%D1%80',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


@dataclass
class RidderParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.RIDDER
    name: str = 'ridder'
    __base_url = 'https://24.kz'
    __news_url = __base_url + '/ru/news/social/itemlist/tag/%D0%A0%D0%B8%D0%B4%D0%B4%D0%B5%D1%80'
    referer = 'https://24.kz/ru/news/social/itemlist/tag/%D0%A0%D0%B8%D0%B4%D0%B4%D0%B5%D1%80'

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
                await asyncio.sleep(random.randrange(3, 8))
                news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.create_session(headers=headers)
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers, session=self.session)
        main_div = soup.find('div', attrs={'id': 'k2Container'})
        if not main_div:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        articles = main_div.find_all('div', class_='col-md-3', limit=15)
        if not articles:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for article in articles:
            div = article.find_next('a')
            url = self.__base_url + div.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title_ = soup.find('h1', class_='single-post__entry-title')
        if not title_:
            return None
        title = title_.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        div = soup.find('div', class_='entry__article')
        div_p = div.find_all('p')
        for p in div_p:
            content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        return image_urls


async def test() -> None:
    parser = RidderParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
