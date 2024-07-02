import asyncio
import contextlib
import re
from dataclasses import dataclass, field

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parsers.models.base import BaseParser
from parsers.models.cities import SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError

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
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/123.0.0.0 Safari/537.36',
}


@dataclass
class AlmataParser(BaseParser):
    request_object: BaseRequest
    headers: dict = field(default_factory=lambda: headers)
    city: SiteModel = SiteModel.ALMATA
    name: str = 'almata'
    __base_url = 'https://www.inalmaty.kz/'
    __news_url = __base_url + 'news'
    referer = 'https://www.inalmaty.kz/news'

    async def get_news(self, urls: list, max_news: int | None = 3) -> list[Post]:
        return await self._get_news(urls=urls, max_news=max_news, headers=self.headers, json=True)

    async def find_news_urls(self, max_news: int = 3) -> list[str]:  # noqa: PLR0912
        self.session: ClientSession = self.request_object.create_session(headers=headers)
        urls = []
        json_url = (
            'https://www.inalmaty.kz/api3/news/{}'
            '?expand=url,title,friendlyPublishDate,sourceReliability,label,isCommercial,isAgeLimited,'
            'isIndexingForbidden,commentsCount,keywordsWithLinks,internalPoster,parsedContent,ratingsInfo,'
            'allowShowCommentsList,allowComment,actualSpecialThemes,author.realName,author.publicName,'
            'author.publicPost,author.authorUrl,author.avatarUrl,poll.question,poll.url,poll.votesCount,'
            'poll.userVote,poll.canUserVote,poll.isActive,poll.answers.answer,poll.answers.votesCount,'
            'commentsPreview.userName,commentsPreview.isAnonymous,commentsPreview.isModerated,'
            'commentsPreview.likesCount,commentsPreview.dislikesCount,commentsPreview.content,'
            'commentsPreview.friendlyPublishDate,commentsPreview.avatarUrl,commentsPreview.isUserLiked,'
            'commentsPreview.isUserDisliked,publishedI18nData.slug'
        )

        try:
            async with self.session:
                soup = await self.request_object.get_soup(url=self.__news_url, session=self.session)
        finally:
            await self.session.close()

        main_articles = soup.find('div', class_='col-12 col-md-8 col-lg-9')
        articles_block = main_articles.find_all(
            'a',
            class_=['c-news-block__title', 'c-news-card__title'],
            limit=max_news // 2,
        )
        if articles_block:
            for article in articles_block:
                try:
                    link_raw = article.get('href')
                    found_link_patterns = re.findall(r'\d+', link_raw)
                    if found_link_patterns:
                        link = found_link_patterns[0]
                        full_link = json_url.format(link)
                        urls.append(full_link)
                except Exception as ex:
                    print(ex)
                    continue
        if not urls:
            raise ParserNoUrlsError(parser_name=self.name, city=str(self.city), source=soup)
        return urls

    def find_photos(self, json_resp: dict) -> list[str]:
        image_urls = []
        with contextlib.suppress(KeyError):
            image_urls.append(json_resp['internalPoster']['url'])
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

    def find_body(self, json_resp: dict) -> str:
        body = ''
        parsed_content = json_resp['parsedContent']
        for content in parsed_content:
            if not content.get('type'):
                continue
            if content['type'] == 'videoBlock':
                continue
            if not content.get('content'):
                continue
            cleantext = BeautifulSoup(content['content'], 'lxml').text
            body += cleantext.replace('\xa0', ' ').strip() + '\n'
        return body

    def find_title(self, json_resp: dict) -> str:
        title = json_resp['title']
        return title


async def test() -> None:
    req_obj = BaseRequest()
    parser = AlmataParser(request_object=req_obj)
    urls = await parser.find_news_urls()
    # print(urls)
    print(await parser.get_news(urls))


if __name__ == '__main__':
    asyncio.run(test())
