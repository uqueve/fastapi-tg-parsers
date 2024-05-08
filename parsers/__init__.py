import logging
from copy import copy
from uuid import uuid4

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.main import send_news
from database.mongo import mongo
from parsers.models.base import BaseParser
from utils.dict_parsers import get_parser_objects
from utils.exceptions.post import PostValidateException
from utils.exceptions.telegram import TelegramSendException
from utils.models import SiteModel, Post, CitySchema

logger = logging.getLogger(__name__)


async def start_parsers():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_news, 'interval', hours=3, name='Парсинг новостей')
    scheduler.add_job(post_news, 'interval', hours=3, name='Постинг новостей')
    scheduler.start()


async def parse_news():
    n = 0
    parsers_objects = get_parser_objects()
    for city in SiteModel:
        try:
            parser_obj: BaseParser = parsers_objects.get(city)

            if not parser_obj:
                continue

            urls: list = await parser_obj.find_news_urls()
            final_urls = copy(urls)
            for url in urls:
                if mongo.is_news_exists_by_link(link=url) is True:
                    final_urls.remove(url)

            if not final_urls:
                logger.warning(f'Нет новостей в городе {str(city)}')
                continue

            news_posts: list[Post] = await parser_obj.get_news(final_urls, max_news=3)

            for post in news_posts:

                if mongo.is_news_exists_by_title(title=post.title) is True:
                    continue

                city_data = mongo.get_city_data_by_city(city=str(city))
                # noinspection PyArgumentList #
                post.city = CitySchema(
                    oid=city_data.get('oid'),
                    name=city_data.get('name'),
                    ru=city_data.get('ru')
                )
                try:
                    post.post_validate()
                except PostValidateException as exception:
                    logger.warning(f'Пост пропущен. Details: {exception.message}')
                    continue
                mongo.add_one_news(post=post)
                n += 1
        except Exception as e:
            logger.exception(f'Error with parsing posts: {e}')
            continue
    logging.info(f'Новостей добавлено за цикл парсинга: {n}')


async def post_news():
    s = 0
    for city in SiteModel:
        try:
            if post := mongo.get_one_not_sent_news(city):
                channel_tg_id = mongo.get_city_tg_id_by_name(city_name=city)
                await send_news(post, channel_tg_id, mongo)
                logging.debug(f'В канал {city} ({channel_tg_id}) отправлена новость: {post.link})')
                s += 1
            else:
                logger.warning(f'Не найдено неотправленных новостей в городе {str(city)}')
        except TelegramSendException as error:
            logging.error(f'{error.message}')
        except Exception as e:
            logging.exception(f'Error with sending posts: {e}')
            continue
    logging.info(f'Новостей отправлено по каналам за цикл: {s}')
