import asyncio
import random
from dataclasses import dataclass

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post, SiteModel

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class UralwebEkatParser(BaseParser, BaseRequest):
    city: SiteModel = SiteModel.EKATERINBURG
    name: str = 'ekaterinburg'
    __base_url = 'https://www.uralweb.ru/'
    __news_url = __base_url + 'news/'
    referer = 'https://www.uralweb.ru/news/'

    async def get_news(self, urls, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
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

    async def find_news_urls(self) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        main_div = soup.find('div', class_='news-box')
        articles = main_div.find_all('li', class_='clearfix', limit=10)
        for article in articles:
            url_raw = article.find_next('div', class_='ln-ann').find('a').get('href').replace('#comments', '')
            url = 'https://www.uralweb.ru' + url_raw
            urls.append(url)
        return urls

    def find_title(self, soup) -> str | None:
        title_ = soup.find('h1')
        if not title_:
            return None
        title = title_.text.replace('\xa0', ' ').strip()
        return title

    def find_body(self, soup) -> str | None:
        content = ''
        div_c = soup.find('div', class_='n-ict clearfix news-detail-body')
        div_p = div_c.find_all('p')
        for p in div_p:
            try:
                content += p.text.replace('\xa0', ' ').strip() + '\n'
            except AttributeError:
                continue
        return content

    def find_photos(self, soup) -> list[str] | list:
        image_urls = []

        photo = soup.find('div', attrs={'id': 'photoblock'})
        if photo:
            photo = photo.find('img')
            if photo:
                photo = photo.get('src').split('?')[0]
                image_urls.append('https:' + photo)
        return image_urls


async def test():
    parser = UralwebEkatParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
