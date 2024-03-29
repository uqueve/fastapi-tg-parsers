import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.main import send_news
from database.mongo import mongo
from parsers.base_parser import BaseParser
from utils.dict_parsers import get_parser_object
from utils.models import SiteModel, Post


logger = logging.getLogger(__name__)


async def start_parsers():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_and_send_posts, 'interval', minutes=3)
    scheduler.start()


async def parse_and_send_posts():
    await parse_news()
    await post_news()


async def parse_news():
    n = 0
    for city in SiteModel:
        try:
            parser_obj: BaseParser = get_parser_object[city]
            news_posts: list[Post] = await parser_obj.get_new_news(max_news=3)
            for post in news_posts:
                if not mongo.is_news_exists_by_link(link=post.link):
                    post.city = city
                    inserted_id = mongo.add_one_news(post=post)
                    logger.debug(f"Добавлена новость {city}")
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
                logging.info(f'В канал {city} ({channel_tg_id}) отправлена новость: {post.link})')
                s += 1
        except Exception as e:
            logging.exception(f'Error with getting and sending posts: {e}')
            continue
    logging.info(f'Новостей отправлено по каналам за цикл: {s}')
