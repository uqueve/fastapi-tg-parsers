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
class PenzaParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.PENZA
    name: str = 'penza'
    __base_url = 'https://www.penzainform.ru'
    __news_url = 'https://www.penzainform.ru/news/'
    referer = 'https://www.penzainform.ru/news/'

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
        alpha_div = soup.find('div', class_='grid_4 alpha')
        if alpha_div and (alpha_img := alpha_div.find('a')):
            if alpha_photo_raw := alpha_img.get('href'):
                alpha_photo = self.__base_url + alpha_photo_raw
                urls.append(alpha_photo)
        omega_div = soup.find('div', class_='grid_4 omega')
        if omega_div and (omega_img := omega_div.find('a')):
            if omega_photo_raw := omega_img.get('href'):
                omega_photo = self.__base_url + omega_photo_raw
                urls.append(omega_photo)
        other_news = soup.find_all('div', class_='gitem grid_8 alpha omega')
        if other_news:
            for new in other_news:
                url = new.find('a')
                if url:
                    url = self.__base_url + url.get('href')
                    urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1')
        if not title:
            return None
        title = title.find('a').get('title').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''
        main_block = soup.find('div', class_='text')
        contents = main_block.find_all('p')
        for con in contents:
            if not con:
                continue
            cleared_con = con.text.replace('\xa0', ' ').strip()
            if find_value(value=cleared_con, example='▶▶'):
                continue
            content += cleared_con + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        image_raw = soup.find('div', class_='img')

        if image_raw:
            photo = image_raw.find('img')
            if not photo:
                return image_urls
            if (photo_url := photo.get('src')) and not photo_url.startswith('http'):
                photo_url = 'https:' + photo_url
            image_urls.append(photo_url)
        return image_urls


def find_value(value: str, example: str) -> bool:
    if value.startswith(example):
        return True
    return False


async def test() -> None:
    parser = PenzaParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
