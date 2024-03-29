import asyncio
import pprint

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class ReportBakuParser(BaseParser):
    name = 'report'
    __base_url = 'https://report.az'
    __news_url = __base_url + '/ru/news-feed/'

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
                await asyncio.sleep(1)
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
        response = await self._make_async_request(url)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')

        title = soup.find('h1', class_='news-title').text.replace('\xa0', ' ').strip()
        print(title)
        # date_tag = soup.find('div', class_='news-date').text.strip().replace('\n', ' ')
        # date = self.parse_date(date_tag)
        date = datetime.now(tz=timezone.utc)

        # if not self.check_is_new_news(last_news_date, date):
        #     return None

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