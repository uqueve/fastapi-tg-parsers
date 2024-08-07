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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://ekaraganda.kz/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


@dataclass
class KaragandaParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.KARAGANDA
    name: str = 'karaganda'
    __base_url = 'https://ekaraganda.kz'
    __news_url = 'https://ekaraganda.kz/'
    referer = 'https://ekaraganda.kz/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url
        try:
            async with self.session:
                soup = await self.request_object.get_soup(url=url, session=self.session)
        finally:
            await self.session.close()
        main_div = soup.find('ul', class_='morelist')
        if not main_div:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        articles = main_div.find_all('li')
        if not articles:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for article in articles:
            div = article.find_next('a')
            url = self.__base_url + div.get('href')
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        main_div = soup.find('div', attrs={'id': 'newsread'})
        if not main_div:
            return None
        title_ = main_div.find('h1')
        if not title_:
            return None
        title = title_.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        div = soup.find('div', class_='read')
        div_p = div.find_all('p')
        for p in div_p:
            if p.text.startswith('Если вы стали свидетелем'):
                return content
            content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        photo_span = soup.find('span', class_='photo')
        if photo_span:
            img = photo_span.find('img').get('src')
            if img.startswith('//'):
                img = 'https:' + img
            image_urls.append(img)
        return image_urls


async def test() -> None:
    parser = KaragandaParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
