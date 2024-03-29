import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

from config_data.config import Settings, setup_settings


def get_mongo_database(settings: Settings) -> Database:
    mongo_client = pymongo.MongoClient(f"mongodb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_ADDRESS}:{settings.DB_PORT}")
    # mongo_client = pymongo.MongoClient(f"mongodb://test_db:test_user@45.142.215.106:27017")
    database: Database = mongo_client[settings.DB_NAME]
    return database


def get_mongo_collection(connection, collection_name) -> Collection:
    collection = connection[collection_name]
    return collection

# get_mongo_collection(settings=setup_settings())
