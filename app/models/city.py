import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Region(Base):
    __tablename__ = 'region'
    name: Mapped[str]
    type: Mapped[str]
    cities: Mapped[list["City"]] = relationship(back_populates='region')


class City(Base):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(sqlalchemy.String, index=True, nullable=False, unique=False)
    post_index: Mapped[int | None]
    utc_offset: Mapped[int]
    lat: Mapped[float]
    lon: Mapped[float]
    population: Mapped[int | None]
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    region: Mapped["Region"] = relationship(back_populates='cities')
