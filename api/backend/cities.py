from fastapi import APIRouter

cities_router = APIRouter(tags=['Cities'])


@cities_router.get('/cities')
async def get_all_cities(): ...
