import asyncio
import pprint
import random
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


headers = {
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}


class UralskParser(BaseParser):
    name = 'uralsk'
    __base_url = 'https://24.kz'
    __news_url = __base_url + '/ru/news/social/itemlist/tag/%D0%A3%D1%80%D0%B0%D0%BB%D1%8C%D1%81%D0%BA'
    referer = 'https://24.kz/ru/news/social/itemlist/tag/%D0%A3%D1%80%D0%B0%D0%BB%D1%8C%D1%81%D0%BA'

    async def get_new_news(self, last_news_date=None, max_news=3) -> [Post]:
        response = await self._make_async_request(self.__news_url, headers=headers)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        main_div = soup.find('section', attrs={'id': 'k2Container'})

        urls = []
        articles = main_div.find_all('div', class_='entry-block', limit=max_news)

        for article in articles:
            try:
                div = article.find_next('a', class_='img-link')
                url = self.__base_url + div.get('href')
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

        pprint.pprint(posts, indent=2)
        return posts

    async def get_new(self, url):
        response = await self._make_async_request(url, referer=self.referer)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')

        title_ = soup.find('h1', class_='entry-title')

        try:
            title = title_.text.replace('\xa0', ' ').strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        div = soup.find('div', class_='entry-content')
        div_p = div.find_all('p')
        for p in div_p:
            content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


if __name__ == '__main__':
    asyncio.run(UralskParser().get_new_news())
