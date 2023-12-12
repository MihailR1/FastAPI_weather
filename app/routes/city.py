from fastapi import APIRouter

from app.utils.crud import CityCRUD
from app.utils.schemas import CitySchema

router = APIRouter(prefix="/city", tags=["Города, данные из БД"])


@router.get("/")
async def get_cities() -> list[CitySchema]:
    """Возвращает все города которые есть в БД"""

    query = await CityCRUD.find_all()
    return query
