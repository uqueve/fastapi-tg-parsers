from database.mongo import connection
from database.mongo.sities import cities


def prepare_database():
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
