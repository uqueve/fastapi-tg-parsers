import asyncio
import random
import re
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


class CherepovecParser(BaseParser):
    name = 'cherepovec'
    __base_url = 'https://cherinfo.ru'
    __news_url = __base_url + '/news'
    referer = 'https://cherinfo.ru/news'

    async def get_new_news(self, last_news_date=None, max_news=3) -> [Post]:
        response = await self._make_async_request(self.__news_url)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')

        main_articles = soup.find('div', class_='container content wrapper')
        articles_block = main_articles.find_all('a', class_='lenta-title', limit=max_news)
        urls = []

        for article in articles_block:
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
        # print(posts)
        return posts

    async def get_new(self, url):
        response = await self._make_async_request(url, headers=headers, referer=self.referer)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(response, 'lxml')

        main_block = soup.find('div', class_='col-lg-9 col-md-9 col-sm-12 col-xs-12 sticky-main print-wide ny-2023')

        if not main_block:
            return

        try:
            title = main_block.find('h1', class_='margin-bottom-small').text.replace('\xa0', ' ').strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        image_urls = set()

        contents_div = main_block.find('div', class_='js-mediator-article article-text')
        contents = contents_div.find_all('p')
        for con in contents:
            photo = con.find('img')
            if photo:
                if photo := photo.get('src'):
                    image_urls.add(photo)
            content += con.text.replace('\xa0', ' ').strip() + '\n'
        if 'Erid' in content:
            return

        photo_div = main_block.find('div', class_='widget print-hidden')

        if photo_div:
            # print(photo_div)
            photos = photo_div.find_all('a')
            for photo in photos:
                if photo := photo.get('href'):
                    image_urls.add(photo)

        image_urls = list(image_urls)
        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


if __name__ == '__main__':
    asyncio.run(CherepovecParser().get_new_news())
