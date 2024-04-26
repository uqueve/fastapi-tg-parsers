import asyncio
import random
from dataclasses import dataclass

from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post


headers = {
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}


@dataclass
class UralskParser(BaseParser, BaseRequest):
    name = 'uralsk'
    __base_url = 'https://24.kz'
    __news_url = __base_url + '/ru/news/social/itemlist/tag/%D0%A3%D1%80%D0%B0%D0%BB%D1%8C%D1%81%D0%BA'
    referer = 'https://24.kz/ru/news/social/itemlist/tag/%D0%A3%D1%80%D0%B0%D0%BB%D1%8C%D1%81%D0%BA'

    async def get_news(self, urls) -> list[Post]:
        news = []
        for new_url in urls:
            if len(news) >= self.max_news:
                return news
            soup = await self.get_soup(new_url, headers=headers, referer=self.referer)
            new = self.get_new(soup, url=new_url)
            if not new:
                continue
            await asyncio.sleep(random.randrange(3, 8))
            news.append(new)
        return news

    async def find_news_urls(self, max_news=3) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        main_div = soup.find('section', attrs={'id': 'k2Container'})

        urls = []
        articles = main_div.find_all('div', class_='entry-block', limit=max_news)

        for article in articles:
            div = article.find_next('a', class_='img-link')
            url = self.__base_url + div.get('href')
            urls.append(url)
        return urls

    def find_title(self, soup) -> str | None:
        title_ = soup.find('h1', class_='entry-title')
        if not title_:
            return None
        title = title_.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ""
        div = soup.find('div', class_='entry-content')
        div_p = div.find_all('p')
        for p in div_p:
            content += p.text.replace('\xa0', ' ').strip() + '\n'
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []
        return image_urls


async def test():
    parser = UralskParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
