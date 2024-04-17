import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.backend.news import news_router
from api.backend.check import health_router
from database.mongo.prepare import prepare_database
from parsers import start_parsers


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@asynccontextmanager
async def lifespan(app_obj: FastAPI):
    prepare_database()
    await start_parsers()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title='News API',
        lifespan=lifespan,
        docs_url='/v1/docs',
        description='API for work with news (FastAPI)',
        debug=False
    )
    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # expose_headers=["*"]
    )
    app.include_router(news_router, prefix='/v1')
    app.include_router(health_router, prefix='/v1')
    return app
