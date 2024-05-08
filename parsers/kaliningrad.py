import asyncio
import random
from dataclasses import dataclass
from bs4 import ResultSet, Tag

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post, SiteModel

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'if-modified-since': 'Sat, 04 May 2024 12:15:01 GMT',
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
class KaliningradParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.KALININGRAD
    name: str = 'kaliningrad'
    __base_url = 'https://kgd.ru'
    __news_url = 'https://kgd.ru/news'
    referer = 'https://kgd.ru/news'

    async def get_news(self, urls, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url, headers=headers, referer=self.referer)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.randrange(8, 15))
            news.append(new)
        return news

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        news = soup.find_all('div', class_='catItemTitle')

        for new in news:
            url = new.find('a')
            if url:
                url = self.__base_url + url.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup) -> str | None:
        title = soup.find('h1', class_='itemTitle')
        if not title:
            return
        title = title.text.strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ""

        main_block = soup.find('div', class_='itemFullText')
        contents = main_block.find_all('p')
        for con in contents:
            if not con:
                continue
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return None
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []
        # print(soup)
        main_photo = soup.find('div', class_='itemImage')
        if main_photo:
            if img_raw := main_photo.find('img'):
                photo = self.__base_url + img_raw.get('src')
                image_urls.append(photo)

        images_raw: ResultSet[Tag] = soup.find_all('a', class_='rsImg')
        if images_raw:
            for img_raw in images_raw:
                if img_raw:
                    img = self.__base_url + img_raw.get('href')
                    image_urls.append(img)
        if len(image_urls) >= 10:
            return image_urls[:9]
        return image_urls


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = KaliningradParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())