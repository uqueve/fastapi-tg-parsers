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
from parsers.models.cities import CitySchema, SiteModel
from parsers.models.posts import Post
from parsers.models.request import BaseRequest
from utils.exceptions.parsers import ParserNoUrlsError
from utils.exceptions.post import PostValidateError
from utils.exceptions.telegram import TelegramSendError

logger = logging.getLogger(__name__)


async def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_news, 'interval', hours=3, name='Парсинг новостей')
    scheduler.add_job(post_news, 'interval', hours=3, jitter=120, name='Постинг новостей')
    scheduler.add_job(clear_old_news, 'cron', day='*', hour=8, name='Очистка старых post: false новостей')
    scheduler.start()
    return scheduler


async def parse_news() -> None:
    urls_count = 0
    posts_count = 0

    not_parsed_posts_parsers = []
    not_parsed_urls_parsers = []

    for _parser_class_str, parser_class in inspect.getmembers(
        object=parsers,
        predicate=inspect.isclass,
    ):
        try:
            request_object = BaseRequest()
            parser_instance: BaseParser = parser_class(request_object=request_object)
            logger.debug("Инициализировал класс реквеста и парсера")
        except Exception:
            logger.exception(f"Ошибка инициализации классов: {_parser_class_str}")
            continue

        logger.debug(f"Собираю ссылки {_parser_class_str}")
        urls_list = await find_urls_for_news(parser_instance=parser_instance)

        if not urls_list:
            logger.warning(f"Не собрал ссылки {_parser_class_str}")
            not_parsed_urls_parsers.append(_parser_class_str)
            continue

        logger.debug(f"Собрал ссылки {_parser_class_str}")

        urls_count += len(urls_list)

        logger.debug(f"Собираю посты {_parser_class_str}")
        posts = await parsing_news(parser_instance=parser_instance, urls=urls_list)

        if not posts:
            logger.warning(f"Не собрал посты {_parser_class_str}")
            not_parsed_posts_parsers.append(_parser_class_str)
            continue

        logger.debug(f"Собрал посты {_parser_class_str}")

        posts_text = ""
        for post in posts:
            posts_text += post.link + ' | '
        logger.debug(f"Для парсера {_parser_class_str} собрались посты: {posts_text}")

        await add_news_to_database(news_posts=posts)

        posts_count += len(posts)
    logger.info(f"Не собрались ссылки: {not_parsed_urls_parsers}")
    logger.info(f"Не собрались посты: {not_parsed_posts_parsers}")
    logger.info(f"Собрано новых ссылок: {urls_count}")
    logger.info(f"Добавлено новых постов в БД: {posts_count}")


async def find_urls_for_news(parser_instance: BaseParser) -> list | None:

    if not parser_instance:
        logger.error("No parser_instance in find_urls_for_news")
        return None

    try:
        urls: list = await parser_instance.find_news_urls()
    except ParserNoUrlsError as error:
        logger.error(f'{error.message}')  # noqa: TRY400
        return None

    final_urls = copy(urls)
    for url in urls:
        if mongo.is_news_exists_by_link(link=url) is True:
            final_urls.remove(url)

    if not final_urls:
        logger.debug(f'Нет новых новостей в городе {parser_instance.city!s}')
    return final_urls


async def parsing_news(parser_instance: BaseParser, urls: list) -> list[Post] | None:
    news_posts: list[Post] = await parser_instance.get_news(
        urls=urls,
        max_news=3,
    )
    if not news_posts:
        logger.warning(f'Не собрались новости по имеющимся ссылкам в городе {parser_instance.city!s}')
        return None
    return news_posts


async def add_news_to_database(news_posts: list[Post]) -> None:

    for post in news_posts:
        try:
            city_data = mongo.get_city_data_by_city(city=str(post.city_model))
        except AttributeError:
            logger.warning(
                f"Нет такого города: {post.city!s}. add_news_to_database. Пост: {post}",
            )
            continue

        if not city_data:
            logger.critical(f'Нет данных по городу {post.city_model}. Новости не постятся.')
            continue
        # noinspection PyArgumentList #
        post.city = CitySchema(
            oid=city_data.get('oid'),
            name=city_data.get('name'),
            ru=city_data.get('ru'),
            local=city_data.get('local'),
        )
        try:
            post.post_validate()
        except PostValidateError as exception:
            logger.warning(f'Пост пропущен. Details: {exception.message}')
            continue

        try:
            mongo.add_one_news(post=post)
        except Exception as e:
            logger.critical(f"Ошибка добавления поста в БД: {e}")
            continue


async def post_news() -> None:
    s = 0
    for city in SiteModel:
        try:
            if post := mongo.get_one_not_sent_news(city):
                channel_tg_id = mongo.get_city_tg_id_by_name(city_name=city)
                logger.debug("Готовлюсь отправлять пост")
                if await send_news(post, channel_tg_id, mongo):

                    logging.debug(
                        f'В канал {city} ({channel_tg_id}) отправлена новость: {post.link})',
                    )
                    s += 1
                else:
                    logger.error(f'Новость в город {city} не была отправлена в канал')
            else:
                logger.debug(f'Не найдено неотправленных новостей в городе {city!s}')
        except TelegramSendError as error:
            logging.exception(f'{error.message}')
            continue
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
