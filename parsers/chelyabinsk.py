import asyncio
import random
from dataclasses import field, dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


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
class ChelyabinskParser(BaseParser, BaseRequest):
    name: str = 'chelyabinsk'
    __base_url: str = 'https://m.ura.news'
    __news_url: str = 'https://m.ura.news/chel'
    referer: str = 'https://m.ura.news/chel'

    async def get_news(self, urls) -> list[Post]:
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url, headers=headers, referer=self.referer)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.randrange(3, 8))
            news.append(new)
        return news

    async def find_news_urls(self, max_news=3) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        main_div = soup.find('div', attrs={'id': 'main_list'})
        items = soup.find_all('div', class_=lambda value: find_value(value, 'list-item'))
        for item in items:
            url_raw = item.find_next('a')
            if not url_raw:
                continue
            url = url_raw.get('href')
            if not url.startswith('https:'):
                url = self.__base_url + url
            urls.append(url)
        return urls

    def find_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('h1', attrs={'itemprop': 'headline name'}).text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup: BeautifulSoup) -> str:
        body = ''
        content = soup.find('div', class_='item-text')
        ps = content.find_all('p')
        for p in ps:
            if not p:
                continue
            if p.text.startswith('Подписка на') or p.text.startswith('Сохрани номер'):
                continue
            body += p.text.replace('\xa0', ' ').strip()
        return body

    def find_photos(self, soup: BeautifulSoup) -> list:
        photos = []
        main_photo_div = soup.find('div', attrs={'itemprop': 'image'})
        if main_photo_div:
            photo = main_photo_div.find('source', attrs={'type': 'image/jpeg'})
            if photo:
                photos.append(photo.get('srcset'))

        other_photos = soup.find_all('div', class_='it-img')
        for photo_div in other_photos:
            photo_raw = photo_div.find('img')
            if not photo_raw:
                continue
            photos.append(photo_raw.get('src'))
        return photos


def find_value(value, example):
    if value:
        if value.startswith(example):
            return True
        return False
    return False


async def test():
    parser = ChelyabinskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
