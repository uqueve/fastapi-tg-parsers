import asyncio
import random

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class UralwebEkatParser(BaseParser):
    name = 'ekaterinburg'
    __base_url = 'https://www.uralweb.ru/'
    __news_url = __base_url + 'news/'
    referer = 'https://www.uralweb.ru/news/'

    async def get_new_news(self, last_news_date=None, max_news=10) -> [Post]:
        response = await self._make_async_request(self.__news_url)
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
        response = await self._make_async_request(url, referer=self.referer)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(await response.text(), 'lxml')

        title_ = soup.find('h1')

        if title_:
            title = title_.text.replace('\xa0', ' ').strip()
        else:
            return None

        # date_tag = soup.find('time', attrs={'itemprop': 'datePublished'}).get('data-utime')
        # date = self.parse_date(date_tag)

        date = datetime.now(tz=timezone.utc)
        # if not self.check_is_new_news(last_news_date, date):
        #     return None

        content = ""
        div_c = soup.find('div', class_='n-ict clearfix news-detail-body')
        div_p = div_c.find_all('p')
        for p in div_p:
            content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        photo = soup.find('div', attrs={'id': 'photoblock'})
        if photo:
            photo = photo.find('img')
            if photo:
                photo = photo.get('src').split('?')[0]
                image_urls.append('https:' + photo)

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post

    def parse_date(self, date_text: str):
        date = datetime.fromtimestamp(float(date_text), tz=timezone.utc)
        return date


if __name__ == '__main__':
    posts = UralwebEkatParser().get_new_news()
    print(posts)