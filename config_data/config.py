import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_URL: str = ''
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASS: str = ''
    DB_NEWS_COLLECTION: str = ''
    TEST_DB_NAME: str = ''

    TG_BOT_TOKEN: str = ''
    ADMIN_IDS: str = ''
    TARGET_CHAT_ID: str = ''
    DISCUSSION_CHAT_ID: str = ''
    YANDEX_PASSPORT_OAUTH_TOKEN: str = ''
    OPENAI_KEY: str = ''
    FASTAPI_API_KEY_HEADER: str = ''


def setup_settings():
    settings = Settings()
    load_dotenv()
    settings.DB_HOST = os.getenv('MONGO_HOST')
    settings.DB_PORT = os.getenv('MONGO_PORT')
    settings.DB_URL = os.getenv('MONGO_URL', '')
    settings.DB_NAME = os.getenv('MONGO_DB', '')
    settings.DB_NEWS_COLLECTION = os.getenv('MONGO_NEWS_COLLECTION', '')
    settings.TEST_DB_NAME = os.getenv('MONGO_TEST_DB', '')
    settings.DB_USER = os.getenv('MONGO_USER')
    settings.DB_PASS = os.getenv('MONGO_PASS')

    settings.TG_BOT_TOKEN = os.environ.get('BOT_TOKEN')
    settings.ADMIN_IDS = os.environ.get('ADMIN_IDS')
    settings.TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_IDS')
    settings.DISCUSSION_CHAT_ID = os.environ.get('DISCUSSION_CHAT_ID')
    settings.YANDEX_PASSPORT_OAUTH_TOKEN = os.environ.get('YANDEX_PASSPORT_OAUTH_TOKEN')
    settings.OPENAI_KEY = os.environ.get('OPENAI_KEY', '')
    settings.FASTAPI_API_KEY_HEADER = os.environ.get(
        'FASTAPI_API_KEY_HEADER',
        'gNLw3lNWgmqQW#@0gfm',
    )
    return settings


@lru_cache
def get_settings():
    settings = setup_settings()
    return settings
