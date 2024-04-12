import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.backend.news import news_router
from database.mongo.prepare import prepare_database
from parsers import start_parsers


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@asynccontextmanager
async def lifespan(app_obj: FastAPI):
    # prepare_database()
    await start_parsers()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title='News API',
        lifespan=lifespan,
        docs_url='/v1/docs',
        description='API for work with news (FastAPI)',
        debug=True
    )
    app.include_router(news_router, prefix='/v1')
    return app
