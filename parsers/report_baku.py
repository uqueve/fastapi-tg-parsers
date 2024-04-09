import asyncio
import pprint
import random

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class ReportBakuParser(BaseParser):
    name = 'baku'
    __base_url = 'https://report.az'
    __news_url = __base_url + '/ru/news-feed/'
    referer = 'https://report.az/ru/'

    async def get_new_news(self, last_news_date=None, max_news=10) -> [Post]:
        response = await self._make_async_request(self.__news_url, json=True)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        json_obj = response
        articles = json_obj['posts']
        urls = []
        for article in articles[:10]:
            try:
                link = self.__base_url + article['url']
                urls.append(link)
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
            return []

        soup = BeautifulSoup(response, 'lxml')

        try:
            title = soup.find('h1', class_='news-title').text.replace('\xa0', ' ').strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        main_div = soup.find('div', class_='editor-body')
        if main_div:
            ps = main_div.find_all('p')
            if ps:
                for p in ps:
                    content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        image = soup.find('div', class_='news-cover')
        if image:
            image = image.find('div', class_='image')
            if image:
                image = image.find('img').get('src')
                image_urls.append(image)

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post

    def parse_date(self, date_text: str):
        date = ' '.join(date_text.split())
        date = dateparser.parse(date, languages=['ru'])
        date = date.replace(tzinfo=timezone.utc)
        return date


if __name__ == '__main__':
    # asyncio.run(ReportBakuParser().get_new('https://report.az/ru/drugie-strany/tramp-ne-pozvolyu-drugim-stranam-otkazatsya-ot-dollara/'))
    asyncio.run(ReportBakuParser().get_new_news())