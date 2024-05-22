import asyncio
import datetime
import inspect
import logging
from copy import copy

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import parsers
from bot.main import send_news
from database.mongo import mongo
from parsers.models.base import BaseParser
from utils.exceptions.parsers import ParserNoUrlsError
from utils.exceptions.post import PostValidateError
from utils.exceptions.telegram import TelegramSendError
from utils.models import CitySchema, Post, SiteModel

logger = logging.getLogger(__name__)


async def start_scheduler() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_news, 'interval', hours=3, name='Парсинг новостей')
    scheduler.add_job(post_news, 'interval', hours=3, name='Постинг новостей')
    scheduler.add_job(clear_old_news, 'cron', day='*', hour=8, name='Очистка старых post: false новостей')
    scheduler.start()


n = 0
not_found_new_urls_cities = []
not_found_urls_cities = []
not_found_news_cities = []


async def parse_news() -> None:
    global n, not_found_news_cities, not_found_urls_cities

    for _parser_class_str, parser_class in inspect.getmembers(
        object=parsers,
        predicate=inspect.isclass,
    ):
        try:
            parser_instance: BaseParser = parser_class()
        except Exception:
            logger.exception(f'{_parser_class_str}')
            continue

        urls_list = await find_urls_for_news(parser_instance=parser_instance)

        if not urls_list:
            continue

        posts = await parsing_news(parser_instance=parser_instance, urls=urls_list)

        if not posts:
            continue

        await add_news_to_database(news_posts=posts)

    logger.info(f'Новостей добавлено за цикл парсинга: {n}')
    logger.info(f'Список городов для которых нет новых ссылок:\n{not_found_new_urls_cities}')
    logger.warning(f'Список городов для которых не собрались ссылки:\n{not_found_urls_cities}')
    logger.warning(f'Список городов для которых не собрались новости по имеющимся ссылкам:\n{not_found_news_cities}')
    n = 0
    not_found_news_cities.clear()
    not_found_urls_cities.clear()


async def find_urls_for_news(parser_instance: BaseParser) -> list | None:
    global not_found_urls_cities
    global not_found_new_urls_cities

    if not parser_instance:
        return None

    try:
        urls: list = await parser_instance.find_news_urls()
    except ParserNoUrlsError as error:
        not_found_urls_cities.append(str(parser_instance.city))
        logger.error(f'{error.message}')
        return None

    final_urls = copy(urls)
    for url in urls:
        if mongo.is_news_exists_by_link(link=url) is True:
            final_urls.remove(url)

    if not final_urls:
        logger.debug(f'Нет новых новостей в городе {parser_instance.city!s}')
        not_found_new_urls_cities.append(str(parser_instance.city))
    return final_urls


async def parsing_news(parser_instance: BaseParser, urls: list) -> list[Post] | None:

    news_posts: list[Post] = await parser_instance.get_news(
        urls=urls,
        max_news=3,
    )
    if not news_posts:
        logger.warning(f'Не собрались новости по имеющимся ссылкам в городе {parser_instance.city!s}')
        not_found_news_cities.append(str(parser_instance.city))
        return None
    return news_posts


async def add_news_to_database(news_posts: list[Post]) -> None:
    global n

    for post in news_posts:
        if mongo.is_news_exists_by_title(title=post.title) is True:
            continue
        try:
            city_data = mongo.get_city_data_by_city(city=str(post.parser_name))
        except AttributeError:
            logger.warning(f'AttributeError. add_news_to_database Пост: {post}')
            continue
            
        if not city_data:
            logger.critical(f'Нет данных по городу {post.parser_name}. Новости не постятся.')
            continue
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
                logger.debug( f'Не найдено неотправленных новостей в городе {city!s}')
        except TelegramSendError as error:
            logging.exception(f'{error.message}')
        except Exception:
            logging.exception('Error with sending posts')
            continue
    logging.info(f'Новостей отправлено по каналам за цикл: {s}')


def clear_old_news() -> None:
    date_delta = datetime.datetime.now() - datetime.timedelta(days=4)
    try:
        mongo.clear_not_posted_news_by_date(date=date_delta)
    except Exception:
        logger.exception('Ошибка очистки новостей')


if __name__ == '__main__':
    asyncio.run(parse_news())
