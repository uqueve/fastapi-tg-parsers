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
    'cache-control': 'max-age=0',
    'dnt': '1',
    'if-none-match': '"10e71-YLSmAWljtVPTiM+MRtLOdr6QQfs"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}


@dataclass
class UstKamenogorskParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.USTKAMENOGORSK
    name: str = 'ustkamenogorsk'
    __base_url: str = 'https://amp.yk-news.kz'
    __news_url: str = 'https://amp.yk-news.kz/'
    referer: str = 'https://amp.yk-news.kz/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        items = soup.find_all('article', class_=lambda v: find_value(v, ' card_item'), limit=15)
        if not items:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for item in items:
            url_raw = item.find_all_next('a')
            if not url_raw:
                continue
            url = url_raw[1].get('href')
            if not url.startswith('https:'):
                url = self.__base_url + url
            urls.append(url)
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1')
        if not title:
            return None
        title = title.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        body = ''
        main_div = soup.find(
            'div',
            class_=lambda v: find_value(v, ' body'),
        )
        if not main_div:
            return
        ps = main_div.find_all('p')
        for p in ps:
            if p.em:
                continue
            body += p.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        main_div = soup.find('div', class_=lambda v: find_value(v, ' article_image'))
        if main_div:
            photo_div = main_div.find('amp-img')
            if photo_div:
                photos.append(photo_div.get('src'))
        main_div = soup.find(
            'div',
            class_=lambda v: find_value(v, ' body'),
        )
        amp_imgs = main_div.find_all('amp-img')
        for amp_img in amp_imgs:
            photos.append(amp_img.get('src'))
        return photos


def find_value(value: str, example: str) -> bool:
    if value:
        if value.endswith(example):
            return True
        return False
    return False


async def test() -> None:
    parser = UstKamenogorskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
