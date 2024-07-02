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
class TagilParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.TAGIL
    name: str = 'tagil'
    __base_url = 'https://v-tagile.ru'
    __news_url = 'https://v-tagile.ru/'
    referer = 'https://v-tagile.ru/'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers)

    async def find_news_urls(self) -> list[str]:
        self.session: ClientSession = self.request_object.create_session(headers=self.headers)
        urls = []
        url = self.__news_url

        async with self.session:
            soup = await self.request_object.get_soup(url=url, session=self.session)

        main_div = soup.find('div', attrs={'id': 'itemListSecondary'})
        if not main_div:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        news_divs = main_div.find_all('div', class_='itemContainer')
        if not news_divs:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for new_div in news_divs:
            new_raw = new_div.find('a')
            if new_raw and (url := new_raw.get('href')):
                urls.append(self.__base_url + url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1')
        if not title:
            return None
        title = title.text.split('\t')[0]
        title = title.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        div = soup.find('div', class_='itemFullText')
        divs = div.find_all('p')
        for p in divs:
            try:
                content += p.text.replace('\xa0', ' ').strip()
            except AttributeError:
                continue
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        main_photo = soup.find('a', class_='itemImage fancybox')
        if main_photo:
            photo_block = main_photo.find('img')
            if photo_block and (photo := photo_block.get('src')):
                image_urls.append(self.__base_url + photo)

        body_div = soup.find('div', class_='itemFullText')
        ps = body_div.find_all('p')
        for p in ps:
            photo_raw = p.find('img')
            if photo_raw and (photo := photo_raw.get('src')):
                image_urls.append(self.__base_url + photo)
        if len(image_urls) >= 10:
            return image_urls[:9]
        return image_urls


async def test() -> None:
    parser = TagilParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
