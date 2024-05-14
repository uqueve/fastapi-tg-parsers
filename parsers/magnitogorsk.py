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
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}


@dataclass
class MagnitogorskParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.MAGNITOGORSK
    name: str = 'magnitogorsk'
    __base_url = 'https://mr-info.ru'
    __news_url = 'https://mr-info.ru/category/news'
    referer = 'https://mr-info.ru/category/news'

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
        news = soup.find_all(
            'article',
            class_=lambda value: find_value(value, 'jeg_post jeg_pl_md_card'),
        )
        if not news:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        for new in news:
            url = new.find('a')
            if url:
                url = url.get('href')
            urls.append(url)
        if not urls:
            await self.session.close()
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str | None:
        title = soup.find('h1', class_='jeg_post_title')
        if not title:
            return None
        title = title.text.strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str | None:
        content = ''

        main_block = soup.find(
            'div',
            class_=lambda value: find_value(value, 'content-inner'),
        )
        if not main_block:
            return None
        contents = main_block.find_all('p')
        for con in contents:
            if not con:
                continue
            if con.text.replace('\xa0', ' ').strip() == 'Фото архив редакции':
                continue
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup: BeautifulSoup) -> list[str] | list:
        image_urls = []
        image_raw = soup.find('div', class_='jeg_featured featured_image ')

        if image_raw:
            photo = image_raw.find('a')
            if not photo:
                return image_urls
            photo = photo.get('src')
            image_urls.append(photo)

        main_block = soup.find(
            'div',
            class_=lambda value: find_value(value, 'content-inner'),
        )
        if not main_block:
            return image_urls
        images_blocks = main_block.find_all('figure', class_='wp-block-image size-full')
        for image_raw in images_blocks:
            if not image_raw:
                continue
            new_image_raw = image_raw.find('img')
            if new_image_raw:
                image = new_image_raw.get('src')
                image_urls.append(image)
        if len(image_urls) >= 10:
            image_urls = image_urls[:9]
        return image_urls


def find_value(value: str, example: str) -> bool:
    if value:
        return bool(value.startswith(example))
    return False


async def test() -> None:
    parser = MagnitogorskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
