from database.mongo import mongo, connection
from utils.models import SiteModel

cities = [
    {'city': SiteModel.URALSK, 'channel_tg_id': -1002014480454},
    {'city': SiteModel.EKATERINBURG, 'channel_tg_id': -1002014480454},
    {'city': SiteModel.ALMATA, 'channel_tg_id': -1002014480454},
    {'city': SiteModel.TASHKENT, 'channel_tg_id': -1002014480454},
    {'city': SiteModel.BAKU, 'channel_tg_id': -1002014480454},
]


def prepare_database():
    colls = connection.list_collection_names()
    if 'news' not in colls:
        connection.create_collection(name='news')
    if 'cities' not in colls:
        connection.create_collection(name='cities')
        collection = connection['cities']
        for city in cities:
            collection.insert_one(document={'name': str(city['city']), 'tg_id': city['channel_tg_id']})


# prepare_database()
