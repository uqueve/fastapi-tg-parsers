import asyncio
import pprint
import random

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class InalmatyAlmataParser(BaseParser):
    name = 'almata'
    __base_url = 'https://www.inalmaty.kz/'
    __news_url = __base_url + 'news'
    referer = 'https://www.inalmaty.kz/news'

    async def get_new_news(self, last_news_date=None, max_news=10) -> [Post]:
        response = await self._make_async_request(self.__news_url)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        main_articles = soup.find('div', class_='col-12 col-md-8 col-lg-9')
        # articles = articles_block.find_all('div', limit=10)
        articles_block = main_articles.find_all('a', class_='c-news-block__title', limit=max_news // 2)
        articles_title = main_articles.find_all('a', class_='c-news-card__title', limit=max_news // 2)
        urls = []
        for article in articles_block:
            try:
                link = article.get('href')
                # link = article.find_next('a').get('href')
                urls.append(link)
            except Exception as ex:
                print(ex)
                continue

        for article in articles_title:
            try:
                link = article.get('href')
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
            return None

        soup = BeautifulSoup(response, 'lxml')

        title_ = soup.find('div', class_='article-details__title-container')

        title = title_.text.replace('\xa0', ' ').strip()

        # date_tag = soup.find('div', class_='article-details__date').text
        # date = self.parse_date(date_tag)
        #
        # if not self.check_is_new_news(last_news_date, date):
        #     return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        main_div = soup.find('div', class_='article-details__text')
        if main_div:
            h4 = main_div.find('h4')
            if h4:
                content += h4.text.replace('\xa0', ' ').strip() + '\n'
            ps = main_div.find_all('p')
            if ps:
                for p in ps:
                    content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post

    def parse_date(self, date_text: str):
        date = ' '.join(date_text.split())
        date = dateparser.parse(date, languages=['ru'])
        date = date.replace(tzinfo=timezone.utc)
        return date


if __name__ == '__main__':
    asyncio.run(InalmatyAlmataParser().get_new_news())
