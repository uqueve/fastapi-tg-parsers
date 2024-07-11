import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.backend.auth import check_api_key
from api.backend.controllers import get_news_by_oid, get_unread_news, set_news_read
from api.backend.models import ErrorSchema, News
from parsers.models.posts import PostOut
from utils.exceptions.api import ApplicationError

logger = logging.getLogger(__name__)
news_router = APIRouter(tags=['News'])


@news_router.get(
    '/news/unread',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': list[PostOut]},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    dependencies=[Depends(check_api_key)],
    description='#### Получение непрочитанных новостей из конкретного города или из всех сразу',
    summary='Получение новостей',
)
async def get_all_news(  # noqa: ANN201
    city: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=30,
            description='##### Наименование города на русском с заглавной буквы. Пример: "Белгород", "Самара"',
        ),
    ] = None,
    limit: Annotated[int | None, Query(description='Лимит')] = 3,
    offset: Annotated[int | None, Query(description='Смещение')] = 0,
):
    try:
        news = get_unread_news(city=city, limit=limit, offset=offset)
    except ApplicationError as ex:
        logger.exception('Problem with getting unread news')
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': ex.message},
        )
    return news


@news_router.get(
    '/news/{oid}',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': PostOut},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    dependencies=[Depends(check_api_key)],
    description='### Получение новости по её oid',
    summary='Получение новости по oid',
)
async def get_one_news_by_oid(  # noqa: ANN201
    oid: Annotated[
        str,
        Path(
            min_length=20,
            max_length=50,
            description='##### Пример: 587092b3-8f0b-4dbe-93a0-a377f030e5bd',
            examples=[
                '587092b3-8f0b-4dbe-93a0-a377f030e5bd',
                '9a2689da-f119-466f-a2bf-a0b2fa84b534',
            ],
        ),
    ],
):
    try:
        news = get_news_by_oid(oid)
    except ApplicationError as ex:
        logger.exception('Problem with getting news by oid')
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': ex.message},
        )
    return news


@news_router.post(
    '/news',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_api_key)],
    description='Отправка новостей по их oid, чтобы пометить их прочитанными. '
    'При последующем запросе всех новостей, прочитанные новости не будут выдаваться',
    responses={
        status.HTTP_201_CREATED: {'model': list[str]},
        status.HTTP_403_FORBIDDEN: {'model': ErrorSchema},
    },
    summary='Пометить новость прочитанной',
)
async def set_read_news(news: News):  # noqa: ANN201
    news_list_read: list = news.ids
    try:
        set_news_read(news_list_read)
    except ApplicationError as ex:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'error': ex.message},
        )

    return {'status': 'ok', 'added_news_ids': news.ids}
