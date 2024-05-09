import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

from config_data.config import Settings


def get_mongo_database(settings: Settings) -> Database:
    # mongo_client = pymongo.MongoClient(
    #     f"mongodb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}")
    mongo_client = pymongo.MongoClient(
        f'mongodb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}',
    )
    database: Database = mongo_client[settings.DB_NAME]
    return database


def get_mongo_collection(connection: Database, collection_name: str) -> Collection:
    collection = connection[collection_name]
    return collection
