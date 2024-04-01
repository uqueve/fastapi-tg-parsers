import asyncio
import pprint

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class GazetaTashkentParser(BaseParser):
    name = 'gazeta'
    __base_url = 'https://www.gazeta.uz/'
    __news_url = __base_url + 'ru/'
    referer = 'https://www.gazeta.uz/ru/'
    # TODO: 503 Service Temporarily Unavailable
    #  'str' object has no attribute 'text'

    async def get_new_news(self, last_news_date=None, max_news=10) -> [Post]:
        response = await self._make_async_request(self.__news_url)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')

        articles_block = soup.find('div', class_='newsblock-2')
        articles = articles_block.find_all('div', class_='nblock', limit=10)
        urls = []

        for article in articles:
            try:
                link = 'https://www.gazeta.uz' + article.find_next('a').get('href')
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

        pprint.pprint(posts, indent=2)
        return posts

    async def get_new(self, url):
        response = await self._make_async_request(url, referer=self.referer)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(response, 'lxml')

        title = soup.find('h1', attrs={'id': 'article_title'}).text.replace('\xa0', ' ').strip()

        # date_tag = soup.find('div', class_='articleDateTime').text.strip().split('\n')[0]
        # date = self.parse_date(date_tag)
        date = datetime.now(tz=timezone.utc)

        # if not self.check_is_new_news(last_news_date, date):
        #     return None

        content = ""

        main_div = soup.find('div', attrs={'itemprop': 'articleBody'})
        ps = main_div.find_all('p')
        for p in ps:
            content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        images = soup.find_all('a', class_='lightbox-img')
        if images:
            for image in images:
                image_urls.append(image.get('href'))

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post

    def parse_date(self, date_text: str):
        date = ' '.join(date_text.split())
        date = dateparser.parse(date, languages=['ru'])
        date = date.replace(tzinfo=timezone.utc)
        return date


if __name__ == '__main__':
    asyncio.run(GazetaTashkentParser().get_new_news())
