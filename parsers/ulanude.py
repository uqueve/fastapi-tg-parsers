import asyncio
import random

from bs4 import BeautifulSoup
from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


class UlanUdeParser(BaseParser):
    name = 'ulanude'
    __base_url = 'https://m.baikal-daily.ru'
    __news_url = __base_url
    referer = 'https://m.baikal-daily.ru/'

    async def get_new_news(self, last_news_date=None, max_news=3) -> [Post]:
        response = await self._make_async_request(self.__news_url, headers=headers)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        urls = []

        news = soup.find_all('div', class_=lambda value: value.startswith('news-item news-item') if value else False)
        # second way to find tags, a more simple to understand
        # news = soup.find_all('div', class_=lambda value: find_value(value))

        for new in news:
            url = self.__base_url + new.find_next('a').get('href')
            urls.append(url)

        for url in urls:
            try:
                post = await self.get_new(url)
                await asyncio.sleep(random.choice(range(5)))
            except Exception as ex:
                continue

            if post is None:
                continue

            posts.append(post)

            if len(posts) >= max_news:
                break

        return posts

    async def get_new(self, url):
        response = await self._make_async_request(url, referer=self.referer)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(response, 'lxml')

        main_block = soup.find('article', class_='news-detail')

        if not main_block:
            return None

        try:
            title = main_block.find('h1').text.strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        content_div = main_block.find('div', class_='news-text')

        if not content_div:
            return None

        content += content_div.text.replace('\xa0', ' ').replace('\r\n', '').strip()
        if 'Erid' in content:
            return None

        image_urls = []
        photo_div = main_block.find('img', class_='preview_picture')

        if photo_div:
            photo = self.__base_url + photo_div.get('src')
            image_urls.append(photo)

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


def find_value(value):
    if value:
        if value.startswith('news-item news-item'):
            return True
        return False
    return False


if __name__ == '__main__':
    asyncio.run(UlanUdeParser().get_new_news())
