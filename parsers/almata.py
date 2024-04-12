import asyncio
import pprint
import random
import re

import dateparser
from dateutil import parser
from bs4 import BeautifulSoup

from datetime import datetime, timezone

from utils.models import Post
from parsers.base_parser import BaseParser


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


class AlmataParser(BaseParser):
    name = 'almata'
    __base_url = 'https://www.inalmaty.kz/'
    __news_url = __base_url + 'news'
    referer = 'https://www.inalmaty.kz/news'

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

    async def get_new(self, url):
        full_url = (f'https://www.inalmaty.kz/api3/news/{url}'
                    f'?expand=url,title,friendlyPublishDate,sourceReliability,label,isCommercial,isAgeLimited,'
                    f'isIndexingForbidden,commentsCount,keywordsWithLinks,internalPoster,parsedContent,ratingsInfo,'
                    f'allowShowCommentsList,allowComment,actualSpecialThemes,author.realName,author.publicName,'
                    f'author.publicPost,author.authorUrl,author.avatarUrl,poll.question,poll.url,poll.votesCount,'
                    f'poll.userVote,poll.canUserVote,poll.isActive,poll.answers.answer,poll.answers.votesCount,'
                    f'commentsPreview.userName,commentsPreview.isAnonymous,commentsPreview.isModerated,'
                    f'commentsPreview.likesCount,commentsPreview.dislikesCount,commentsPreview.content,'
                    f'commentsPreview.friendlyPublishDate,commentsPreview.avatarUrl,commentsPreview.isUserLiked,'
                    f'commentsPreview.isUserDisliked,publishedI18nData.slug')
        response = await self._make_async_request(full_url, json=True, headers=headers)

        if not response:
            print(f"Ошибка запроса {__name__}")
            return None

        body = ''
        image_urls = []

        try:
            image_urls.append(response['internalPoster']['url'])
        except KeyError:
            pass

        parsed_content = response['parsedContent']
        for content in parsed_content:
            if not content.get('type'):
                continue
            if content['type'] == 'imageBlock':
                image_urls.append(content['sourceUrl'])
            if content['type'] == 'videoBlock':
                continue
            if not content.get('content'):
                continue
            cleantext = BeautifulSoup(content['content'], "lxml").text
            body += cleantext.replace('\xa0', ' ').strip() + '\n'

        link = response['url']
        title = response['title']
        date = datetime.now(tz=timezone.utc)

        post = Post(title=title, body=body, image_links=image_urls, date=date, link=link)
        return post


if __name__ == '__main__':
    asyncio.run(AlmataParser().get_new_news())
