from fastapi import APIRouter, status, Depends, HTTPException

from api.backend.controllers import *
from utils.exceptions.api import ApplicationException
from utils.models import News, PostOut, ErrorSchema
from api.backend.auth import check_api_key

news_router = APIRouter(tags=['News'])


@news_router.get('/news/unread',
                 status_code=status.HTTP_200_OK,
                 responses={status.HTTP_200_OK: {'model': list[PostOut]},
                            status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}},
                 dependencies=[Depends(check_api_key)],
                 description='Получение непрочитанных новостей')
async def get_all_news():
    try:
        news = get_unread_news()
    except ApplicationException as ex:
        logger.exception('Problem with getting unread news')
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': ex.message})
    return news


@news_router.post('/news',
                  status_code=status.HTTP_201_CREATED,
                  dependencies=[Depends(check_api_key)],
                  description='Отправка новостей по их oid, чтобы пометить их прочитанными. '
                              'При последующем запросе всех новостей, прочитанные новости не будут выдаваться',
                  responses={status.HTTP_201_CREATED: {'model': list[str]},
                             status.HTTP_403_FORBIDDEN: {'model': ErrorSchema}})
async def set_read_news(news: News):
    news_list_read: list = news.ids
    try:
        set_news_read(news_list_read)
    except ApplicationException as ex:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'error': ex.message})

    return {
        'status': 'ok',
        'added_news_ids': news.ids
    }
