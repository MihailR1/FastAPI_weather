from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.__class__.__name__} - id={self.id}'


class City(Base):
    __tablename__ = "city"

    country: Mapped[str]
    region: Mapped[str]
    name: Mapped[str] = mapped_column(sqlalchemy.String, index=True, nullable=False, unique=False)
    latitude: Mapped[float]
    longitude: Mapped[float]
    weather: Mapped['Weather'] = relationship(back_populates='city', uselist=False)


class Weather(Base):
    __tablename__ = "weather"

    temperature: Mapped[float]
    feels_like: Mapped[float]
    pressure: Mapped[float]
    humidity: Mapped[float]
    wind_speed: Mapped[float]

    city_id: Mapped['City'] = mapped_column(sqlalchemy.ForeignKey('city.id'))
    city: Mapped['City'] = relationship(back_populates='weather', uselist=False)
