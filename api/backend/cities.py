from fastapi import APIRouter, status, Depends, HTTPException

from api.backend.controllers import *
from utils.models import News, PostOut
from api.backend.auth import check_api_key

cities_router = APIRouter(tags=['Cities'])


@cities_router.get('/cities')
async def get_all_cities():
    ...
