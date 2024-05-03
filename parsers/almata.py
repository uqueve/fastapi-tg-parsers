import asyncio
import pprint
import random
import re
from dataclasses import dataclass

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from parsers.models.base import BaseParser
from parsers.models.request import BaseRequest
from utils.models import Post

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-KZ,ru',
    'dnt': '1',
    'referer': 'https://www.inalmaty.kz/news',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class AlmataParser(BaseParser, BaseRequest):
    name = 'almata'
    __base_url = 'https://www.inalmaty.kz/'
    __news_url = __base_url + 'news'
    referer = 'https://www.inalmaty.kz/news'

    async def get_news(self, urls, max_news: int | None = None) -> list[Post]:
        if max_news:
            self.max_news = max_news
        news = []
        for url in urls:
            if len(news) >= self.max_news:
                return news
            json_url = (f'https://www.inalmaty.kz/api3/news/{url}'
                        f'?expand=url,title,friendlyPublishDate,sourceReliability,label,isCommercial,isAgeLimited,'
                        f'isIndexingForbidden,commentsCount,keywordsWithLinks,internalPoster,parsedContent,ratingsInfo,'
                        f'allowShowCommentsList,allowComment,actualSpecialThemes,author.realName,author.publicName,'
                        f'author.publicPost,author.authorUrl,author.avatarUrl,poll.question,poll.url,poll.votesCount,'
                        f'poll.userVote,poll.canUserVote,poll.isActive,poll.answers.answer,poll.answers.votesCount,'
                        f'commentsPreview.userName,commentsPreview.isAnonymous,commentsPreview.isModerated,'
                        f'commentsPreview.likesCount,commentsPreview.dislikesCount,commentsPreview.content,'
                        f'commentsPreview.friendlyPublishDate,commentsPreview.avatarUrl,commentsPreview.isUserLiked,'
                        f'commentsPreview.isUserDisliked,publishedI18nData.slug')
            soup = await self.get_json(
                url=json_url,
                json=True,
                headers=headers,
                referer=self.referer)
            new = self.get_new(
                soup,
                url=json_url,
            )
            if not new:
                continue
            await asyncio.sleep(random.randrange(3, 5))
            news.append(new)
        return news

    async def find_news_urls(self, max_news=3) -> list[str]:
        urls = []
        url = self.__news_url
        soup = await self.get_soup(url=url, headers=headers)
        main_articles = soup.find('div', class_='col-12 col-md-8 col-lg-9')
        articles_block = main_articles.find_all('a', class_='c-news-block__title', limit=max_news // 2)
        articles_title = main_articles.find_all('a', class_='c-news-card__title', limit=max_news // 2)
        urls = []
        for article in articles_block:
            try:
                link_raw = article.get('href')
                found_link_patterns = re.findall(r"\d+", link_raw)
                if found_link_patterns:
                    link = found_link_patterns[0]
                    urls.append(link)
            except Exception as ex:
                print(ex)
                continue

        for article in articles_title:
            try:
                link_raw = article.get('href')
                found_link_patterns = re.findall(r"\d+", link_raw)
                if found_link_patterns:
                    link = found_link_patterns[0]
                    urls.append(link)
            except Exception as ex:
                print(ex)
                continue
        return urls

    async def get_new_news(self, last_news_date=None, max_news=6) -> [Post]:
        response = await self._make_async_request(self.__news_url)
        posts = []

        if not response:
            print(f"Ошибка запроса {__name__}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        main_articles = soup.find('div', class_='col-12 col-md-8 col-lg-9')
        articles_block = main_articles.find_all('a', class_='c-news-block__title', limit=max_news // 2)
        articles_title = main_articles.find_all('a', class_='c-news-card__title', limit=max_news // 2)
        urls = []
        for article in articles_block:
            try:
                link_raw = article.get('href')
                found_link_patterns = re.findall(r"\d+", link_raw)
                if found_link_patterns:
                    link = found_link_patterns[0]
                    urls.append(link)
            except Exception as ex:
                print(ex)
                continue

        for article in articles_title:
            try:
                link_raw = article.get('href')
                found_link_patterns = re.findall(r"\d+", link_raw)
                if found_link_patterns:
                    link = found_link_patterns[0]
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

    def find_photos(self, json_resp) -> list[str]:
        image_urls = []
        try:
            image_urls.append(json_resp['internalPoster']['url'])
        except KeyError:
            pass
        parsed_content = json_resp['parsedContent']
        for content in parsed_content:
            if not content.get('type'):
                continue
            if content['type'] == 'imageBlock':
                image_urls.append(content['sourceUrl'])
            if content['type'] == 'videoBlock':
                continue
            if not content.get('content'):
                continue
        return image_urls

    def find_body(self, json_resp) -> str:
        body = ''
        parsed_content = json_resp['parsedContent']
        for content in parsed_content:
            if not content.get('type'):
                continue
            if content['type'] == 'videoBlock':
                continue
            if not content.get('content'):
                continue
            cleantext = BeautifulSoup(content['content'], "lxml").text
            body += cleantext.replace('\xa0', ' ').strip() + '\n'
        return body

    def find_title(self, json_resp) -> str:
        # link = json_resp['url']
        title = json_resp['title']
        return title


async def test():
    parser = AlmataParser()
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
