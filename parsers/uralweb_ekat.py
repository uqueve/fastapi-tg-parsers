import asyncio
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class UralwebEkatParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.EKATERINBURG
    name: str = 'ekaterinburg'
    __base_url = 'https://www.uralweb.ru/'
    __news_url = __base_url + 'news/'
    referer = 'https://www.uralweb.ru/news/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        main_div = soup.find('div', class_='news-box')
        if not main_div:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        articles = main_div.find_all('li', class_='clearfix', limit=10)
        if not articles:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for article in articles:
            url_raw = article.find_next('div', class_='ln-ann').find('a').get('href').replace('#comments', '')
            url = 'https://www.uralweb.ru' + url_raw
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title_ = soup.find('h1')
        if not title_:
            return None
        title = title_.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        div_c = soup.find('div', class_='n-ict clearfix news-detail-body')
        div_p = div_c.find_all('p')
        for p in div_p:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError:
                continue
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []

        photo = soup.find('div', attrs={'id': 'photoblock'})
        if photo:
            photo = photo.find('img')
            if photo:
                photo = photo.get('src').split('?')[0]
                image_urls.append('https:' + photo)
        return image_urls


async def test() -> None:
    parser = UralwebEkatParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
