from pymongo.collection import Collection
from pymongo.database import Database

from config_data.config import setup_settings, Settings
from database.mongo.connection import get_mongo_collection, get_mongo_database
from database.mongo.repository import NewsRepository

settings: Settings = setup_settings()
connection: Database = get_mongo_database(settings=settings)
mongo = NewsRepository(connection=connection)