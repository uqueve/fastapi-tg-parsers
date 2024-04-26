import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


@dataclass
class TashkentParser(BaseParser, BaseRequest):
    name = 'tashkent'
    __base_url = 'https://www.gazeta.uz/'
    __news_url = __base_url + 'ru/'
    referer = 'https://www.gazeta.uz/ru/'

    async def get_news(self, urls) -> list[Post]:
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url, referer=self.referer)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.randrange(3, 8))
            news.append(new)
        return news

    async def find_news_urls(self, max_news=3) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url)
        articles_block = soup.find('div', class_='newsblock-2')
        articles = articles_block.find_all('div', class_='nblock', limit=10)
        urls = []

        for article in articles:
            link = 'https://www.gazeta.uz' + article.find_next('a').get('href')
            urls.append(link)
        return urls

    def find_title(self, soup) -> str | None:
        title = soup.find('h1', attrs={'id': 'article_title'}).text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ""

        main_div = soup.find('div', attrs={'itemprop': 'articleBody'})
        ps = main_div.find_all('p')
        for p in ps:
            content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []

        images = soup.find_all('a', class_='lightbox-img')
        if images:
            for image in images:
                image_urls.append(image.get('href'))
        return image_urls


async def test():
    parser = TashkentParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
