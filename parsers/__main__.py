import asyncio
import inspect
import logging
from copy import copy

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import parsers
from bot.main import send_news
from database.mongo import mongo
from parsers.models.base import BaseParser
from utils.exceptions.post import PostValidateError
from utils.exceptions.telegram import TelegramSendError
from utils.models import CitySchema, Post, SiteModel

logger = logging.getLogger(__name__)


async def start_parsers() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_news, 'interval', hours=3, name='Парсинг новостей')
    scheduler.add_job(post_news, 'interval', hours=3, name='Постинг новостей')
    scheduler.start()


async def parse_news() -> None:
    n = 0
    for _parser_class_str, parser_class in inspect.getmembers(
        parsers,
        predicate=inspect.isclass,
    ):
        try:
            parser_instance: BaseParser = parser_class()

            if not parser_instance:
                continue

            urls: list = await parser_instance.find_news_urls()
            final_urls = copy(urls)
            for url in urls:
                if mongo.is_news_exists_by_link(link=url) is True:
                    final_urls.remove(url)

            if not final_urls:
                logger.warning(f'Нет новостей в городе {parser_instance.city!s}')
                continue

            news_posts: list[Post] = await parser_instance.get_news(
                final_urls,
                max_news=3,
            )

            for post in news_posts:
                if mongo.is_news_exists_by_title(title=post.title) is True:
                    continue

                city_data = mongo.get_city_data_by_city(city=str(parser_instance.city))
                # noinspection PyArgumentList #
                post.city = CitySchema(
                    oid=city_data.get('oid'),
                    name=city_data.get('name'),
                    ru=city_data.get('ru'),
                )
                try:
                    post.post_validate()
                except PostValidateError as exception:
                    logger.warning(f'Пост пропущен. Details: {exception.message}')
                    continue
                mongo.add_one_news(post=post)
                n += 1
        except Exception:
            logger.exception('Error with parsing posts')
            continue
    logging.info(f'Новостей добавлено за цикл парсинга: {n}')


async def post_news() -> None:
    s = 0
    for city in SiteModel:
        try:
            if post := mongo.get_one_not_sent_news(city):
                channel_tg_id = mongo.get_city_tg_id_by_name(city_name=city)
                await send_news(post, channel_tg_id, mongo)
                logging.debug(
                    f'В канал {city} ({channel_tg_id}) отправлена новость: {post.link})',
                )
                s += 1
            else:
                logger.warning(
                    f'Не найдено неотправленных новостей в городе {city!s}',
                )
        except TelegramSendError as error:
            logging.exception(f'{error.message}')
        except Exception:
            logging.exception('Error with sending posts')
            continue
    logging.info(f'Новостей отправлено по каналам за цикл: {s}')


if __name__ == '__main__':
    asyncio.run(parse_news())
