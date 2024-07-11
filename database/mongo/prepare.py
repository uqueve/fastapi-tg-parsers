import logging

from database.mongo import connection
from database.mongo.sities import get_actual_cities_json

logger = logging.getLogger(__name__)


def prepare_database() -> None:
    logger.debug('Подготовка базы данных')

    colls = connection.list_collection_names()
    if 'news' not in colls:
        connection.create_collection(name='news')
    if 'cities' not in colls:
        connection.create_collection(name='cities')

    collection = connection['cities']

    cities: dict = get_actual_cities_json()
    for city_model, city_info in cities.items():

        if not collection.find_one(filter={'name': str(city_model)}):
            collection.insert_one(
                document={
                    'oid': str(city_info['oid']),
                    'name': str(city_info['city']),
                    'tg_id': int(city_info['channel_tg_id']),
                    'ru': city_info['ru'],
                    'local': city_info['local'],
                },
            )
