from fastapi import FastAPI

from app.routes.city import router as city_router
from app.routes.weather import router as weather_router

app = FastAPI()

app.include_router(city_router)
app.include_router(weather_router)
