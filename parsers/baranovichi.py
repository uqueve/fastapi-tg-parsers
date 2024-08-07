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
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


@dataclass
class BaranovichiParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.BARANOVICHI
    name: str = 'baranovichi'
    __base_url = 'https://baranovichi-gik.gov.by'
    __news_url = 'https://baranovichi-gik.gov.by/ru/news-ru'
    referer = 'https://baranovichi-gik.gov.by/ru/news-ru'

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
        news = soup.find_all('div', class_='news_title')
        if not news:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for new in news:
            url_block = new.find('a')
            if not url_block:
                continue
            url = url_block.get('href')
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        main_block = soup.find('div', class_='news_inner')
        title = main_block.find('h2').text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        main_block = soup.find('div', class_='news_inner_one_text')
        contents = main_block.find_all('p')
        for con in contents:
            if 'Корр. БЕЛТА' in con.text:
                con_list = con.text.split('.')
                if len(con_list) > 2:
                    con = '.'.join(con_list[2:])
                    content += con.replace('\xa0', ' ').strip() + '\n'
                    continue
                else:
                    continue
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        main_block = soup.find('div', class_='news_inner_one_text')
        all_images = main_block.find_all('img')
        for img in all_images:
            image_raw = img.get('src')
            image_urls.append(image_raw)
        return image_urls


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = BaranovichiParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
