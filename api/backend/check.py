from fastapi import APIRouter, status, Depends

from api.backend.auth import check_api_key


health_router = APIRouter(tags=['Health'])


@health_router.get('/health',
                   status_code=status.HTTP_200_OK,
                   description='Тест работы бэкенда')
async def check_health():
    return {'status': 'ok'}


@health_router.get('/health-apikey',
                   status_code=status.HTTP_200_OK,
                   dependencies=[Depends(check_api_key)],
                   description='Проверка подключения к бэкенду по apikey')
async def check_health_apikey():
    return {'status': 'ok'}
