import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends, HTTPException

from api.backend.auth import check_api_key
from api.backend.controllers import *
from database.mongo.prepare import prepare_database
from parsers import start_parsers
from utils.models import News, PostOut

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@asynccontextmanager
async def lifespan(app_obj: FastAPI):
    prepare_database()
    await start_parsers()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/v1/health',
         status_code=status.HTTP_200_OK)
async def check_health():
    return {'status': 'ok'}


@app.get('/v1/health-apikey',
         status_code=status.HTTP_200_OK,
         dependencies=[Depends(check_api_key)])
async def check_health_apikey():
    return {'status': 'ok'}


@app.get('/v1/news/all',
         status_code=status.HTTP_200_OK,
         response_model=list[PostOut],
         dependencies=[Depends(check_api_key)])
async def get_all_news():
    news = get_unread_news()
    return news


@app.post('/v1/news', status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_api_key)])
async def set_read_news(news: News):
    news_list_read: list = news.ids
    if set_news_read(news_list_read):
        return {
            'status': 'ok',
            'added_news_ids': news.ids
        }
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Something went wrong')
