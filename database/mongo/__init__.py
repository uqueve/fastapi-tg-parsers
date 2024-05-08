from pymongo.database import Database

from config_data.config import get_settings, Settings
from database.mongo.connection import get_mongo_database
from database.mongo.repository import NewsRepository

settings: Settings = get_settings()
connection: Database = get_mongo_database(settings=settings)
mongo = NewsRepository(connection=connection)
