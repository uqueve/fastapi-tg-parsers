import asyncio
import pprint
import random
from bs4 import BeautifulSoup
from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


class MgorodUralskParser(BaseParser):
    name = 'uralsk'
    __base_url = 'https://mgorod.kz/'
    __news_url = __base_url + 'nlocation/uralsk/'
    referer = 'https://mgorod.kz/nlocation/uralsk/'
    # TODO: 403 Enable JavaScript and cookies to continue Just a moment...
    # TODO: Заменить парсер

    async def get_new_news(self, last_news_date=None, max_news=3) -> [Post]:
        response = await self._make_async_request(self.__news_url)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        main_div = soup.find('div', class_='news news-home-block-list news-latest')

        urls = []
        articles = main_div.find_all('div', class_='news-item-in', limit=5)

        for article in articles:
            try:
                div = article.find_next('a', class_='news-link-in-single')
                url = div.get('href')
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

        title_ = soup.find('h1', class_='news-title h1')

        try:
            title = title_.text.replace('\xa0', ' ').strip()
        except AttributeError:
            print(f'Title not find in {__name__}. URL: {url}')
            return None

        date = datetime.now(tz=timezone.utc)

        content = ""
        div = soup.find('div', class_='news-single-sector news-single-content')
        div_p = div.find_all('p')
        for p in div_p:
            content += p.text.replace('\xa0', ' ').strip() + '\n'

        image_urls = []

        photo = soup.find('div', class_='news-image news-main-image news-single-sector')
        if photo:
            photo = photo.find('img')
            if photo:
                image_urls.append(photo.get('src'))

        post = Post(title=title, body=content, image_links=image_urls, date=date, link=url)
        return post


if __name__ == '__main__':
    asyncio.run(MgorodUralskParser().get_new_news())
