from fastapi import APIRouter

from app.utils.crud import CityCRUD

router = APIRouter(prefix="/city", tags=["Города, данные из БД"])


@router.get("")
async def get_cities():
    """Возвращает все города которые есть в БД"""

    query = await CityCRUD.find_all()
    return query
