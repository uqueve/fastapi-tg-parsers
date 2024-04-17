import asyncio
import json
import pprint
import random

from bs4 import BeautifulSoup
from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


headers = {
    'AMP-Same-Origin': 'true',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://ria.ru/amp/location_Tallinn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-gpc': '1',
}


class TallinTallinParser(BaseParser):
    name = 'tallin'
    __base_url = 'https://ria.ru'
    __news_url = __base_url + '/amp/location_Tallinn/more.json'
    referer = 'https://ria.ru/amp/location_Tallinn/'

    async def get_new_news(self, last_news_date=None, max_news=3) -> [Post]:
        response = await self._make_async_request(self.__news_url, headers=headers, json=True)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        urls = []
        for new in response['items']:
            urls.append(new['url'])

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
        response = await self._make_async_request(url)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        soup = BeautifulSoup(response, 'lxml')

        try:
            title = soup.find(['div', 'h1'], class_='article__title').text.strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        div = soup.find('div', class_='article__body js-mediator-article mia-analytics')
        divs = div.find_all('div', 'article__block')
        for p in divs:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError as ex:
                continue

        image_urls = []
        photo_div = soup.find('div', class_='article__announce')
        photo_div = photo_div.find('div', class_='photoview__open')
        data = [json.loads(script.text) for script in photo_div.find_all('script', type='application/ld+json')]

        # TODO: WEBP > JPG ?
        if data:
            photo = data[-1]['url']
            image_urls.append(photo)

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


if __name__ == '__main__':
    pprint.pprint(asyncio.run(TallinTallinParser().get_new_news()))
