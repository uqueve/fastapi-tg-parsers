import asyncio
import random

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


class UralwebEkatParser(BaseParser):
    name = 'ekaterinburg'
    __base_url = 'https://www.uralweb.ru/'
    __news_url = __base_url + 'news/'
    referer = 'https://www.uralweb.ru/news/'

    async def get_new_news(self, last_news_date=None, max_news=10) -> [Post]:
        response = await self._make_async_request(self.__news_url, headers=headers)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')

        main_div = soup.find('div', class_='news-box')
        articles = main_div.find_all('li', class_='clearfix', limit=10)
        urls = []
        for article in articles:
            try:
                url_raw = article.find_next('div', class_='ln-ann').find('a').get('href').replace('#comments', '')
                url = 'https://www.uralweb.ru' + url_raw
                urls.append(url)
            except Exception as ex:
                print(ex)
                continue

        for url in urls:
            try:
                post = await self.get_new(url)
                await asyncio.sleep(random.choice(range(5)))
            except Exception as ex:
                print(ex)
                continue

            if post is None:
                continue

            posts.append(post)

            if len(posts) >= max_news:
                break

        return posts

    async def get_new(self, url):
        response = await self._make_async_request(url, referer=self.referer, headers=headers)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(response, 'lxml')
        title_ = soup.find('h1')

        try:
            title = title_.text.replace('\xa0', ' ').strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        div_c = soup.find('div', class_='n-ict clearfix news-detail-body')
        div_p = div_c.find_all('p')
        for p in div_p:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError:
                continue

        image_urls = []

        photo = soup.find('div', attrs={'id': 'photoblock'})
        if photo:
            photo = photo.find('img')
            if photo:
                photo = photo.get('src').split('?')[0]
                image_urls.append('https:' + photo)

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


if __name__ == '__main__':
    asyncio.run(UralwebEkatParser().get_new_news(max_news=1))