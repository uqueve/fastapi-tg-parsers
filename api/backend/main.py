import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.backend.check import health_router
from api.backend.news import news_router
from database.mongo.prepare import prepare_database
from parsers.__main__ import start_scheduler


def setup_logger():
    logging.basicConfig(
        level=logging.INFO, stream=sys.stdout, format='%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s.%(funcName)s:%(lineno)d - %(message)s'
    )


@asynccontextmanager
async def lifespan(app_obj: FastAPI):
    setup_logger()
    # ruff: noqa
    prepare_database()
    await start_scheduler()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title='News API',
        lifespan=lifespan,
        docs_url='/v1/docs',
        description='API for work with news (FastAPI)',
        debug=False,
    )
    origins = [
        '*',
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        # expose_headers=["*"]
    )
    app.include_router(news_router, prefix='/v1')
    app.include_router(health_router, prefix='/v1')
    return app
