import asyncio
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
    'application/signed-exchange;v=b3;q=0.7',
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
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/124.0.0.0 Safari/537.36',
}


@dataclass
class SalvadorParser(BaseParser):
    request_object: BaseRequest
    city: SiteModel = SiteModel.SALVADOR
    name: str = 'salvador'
    __base_url: str = 'https://cnnespanol.cnn.com'
    __news_url: str = 'https://cnnespanol.cnn.com/category/centroamerica/el-salvador/'
    referer: str = 'https://cnnespanol.cnn.com/category/centroamerica/el-salvador/'
    headers: dict = field(default_factory=lambda: headers)

    # async def get_news(self, urls: list, max_news: int | None = None) -> list[Post]:
    #     self.session: ClientSession = self.request_object.create_session(headers=self.headers)
    #     if max_news:
    #         self.max_news = max_news
    #     news = []
    #     try:
    #         async with self.session:
    #             for new_url in urls:
    #                 if len(news) >= self.max_news:
    #                     return news
    #                 soup = await self.request_object.get_soup(session=self.session, url=new_url)
    #                 new = self.get_new(soup, url=new_url)
    #                 if not new:
    #                     continue
    #                 await asyncio.sleep(random.randrange(8, 15))
    #                 news.append(new)
    #     finally:
    #         await self.session.close()
    #     return news

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url
        try:
            async with self.session:
                soup = await self.request_object.get_soup(url=url, session=self.session)
        finally:
            await self.session.close()

        items = soup.find_all('h2', class_='news__title', limit=3)
        if not items:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_next('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('https:'):
                url = self.__base_url + url
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', class_=['news__title', 'storyfull__title'])
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        divs = soup.find(
            'div',
            class_=['storyfull__body', 'news__excerpt'],
        )
        ps = divs.find_all('p')
        for p in ps:
            body += p.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        main_div = soup.find(
            'div',
            class_='storyfull__gallery',
        )
        if not main_div:
            return photos
        photo_divs = main_div.find_all('img', 'image')
        for photo_div in photo_divs:
            if photo_div:
                photo = photo_div.get('src')
                photos.append(photo)
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test() -> None:
    request_obj = BaseRequest()
    parser = SalvadorParser(request_object=request_obj)
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
