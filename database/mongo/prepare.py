from database.mongo import connection, NewsRepository
from database.mongo.sities import cities
from utils.models import SiteModel


def prepare_database():
    # db = NewsRepository(connection=connection)
    #
    # for city in cities:
    #     new = db.get_one_not_sent_news(str(city['city']))
    #     if new:
    #         print(new)
    #     else:
    #         print(f'Не найдено неотправленных новостей в городе {str(city)}')
    # city = SiteModel.NOVOKUZNETSK
    # print(db.get_city_data_by_city(city=city))
    # news = db._get_all_news()
    # for new in news:
    #     print(new)
    # cities1 = db._get_all_cities()
    # for city in cities1:
    #     print(city)

    colls = connection.list_collection_names()
    if 'news' not in colls:
        connection.create_collection(name='news')
    if 'cities' not in colls:
        connection.create_collection(name='cities')
    collection = connection['cities']
    for city in cities:
        if not collection.find_one(filter={'name': str(city['city'])}):
            collection.insert_one(
                document={
                    'oid': str(city['oid']),
                    'name': str(city['city']),
                    'tg_id': int(city['channel_tg_id']),
                    'ru': city['ru'],
                }
            )
