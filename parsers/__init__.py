import logging
from uuid import uuid4

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.main import send_news
from database.mongo import mongo
from parsers.base_parser import BaseParser
from utils.dict_parsers import get_parser_object
from utils.models import SiteModel, Post, CitySchema

logger = logging.getLogger(__name__)


async def start_parsers():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_news, 'interval', minutes=10, name='Парсинг новостей')
    scheduler.add_job(post_news, 'interval', minutes=10, name='Постинг новостей')
    scheduler.start()


async def parse_news():
    n = 0
    for city in SiteModel:
        try:
            print(f'Перед парсингом города {str(city)}')
            parser_obj: BaseParser = get_parser_object[city]
            news_posts: list[Post] = await parser_obj.get_new_news(max_news=3)
            if not news_posts:
                print(f'Нет новостей в городе {str(city)}')
                continue
            print(f'Собраны посты в городе {str(city)}\t{news_posts}')
            for post in news_posts:
                print('Перед добавлением в БД')
                if not mongo.is_news_exists_by_link(link=post.link):
                    print('Новость не существует')
                    city_data = mongo.get_city_data_by_city(city=city)
                    post.city = CitySchema(
                        oid=city_data.get('oid'),
                        name=city_data.get('name'),
                        ru=city_data.get('ru')
                    )
                    post.oid = str(uuid4())
                    print('Прямо перед добавлением')
                    mongo.add_one_news(post=post)
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
            else:
                print(f'Не найдено неотправленных новостей в городе {str(city)}')
        except Exception as e:
            logging.exception(f'Error with getting and sending posts: {e}')
            continue
    logging.info(f'Новостей отправлено по каналам за цикл: {s}')
