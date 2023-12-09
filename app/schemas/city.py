from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str
    post_index: int
    utc_offset: str
    latitude: float
    longitude: float
    population: int
    region_id: int

    class Config:
        orm_mode = True


class RegionScheme(BaseModel):
    name: str
    type: str
    cities: list['CitySchema']

    class Config:
        orm_mode = True
