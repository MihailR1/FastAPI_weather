from pydantic import BaseModel, Field, AliasPath


class CitySchema(BaseModel):
    country: str = Field(validation_alias=AliasPath(
        'metaDataProperty',
        'GeocoderMetaData',
        'AddressDetails',
        'Country',
        'CountryName'
    ))
    region: str = Field(validation_alias=AliasPath(
        'metaDataProperty',
        'GeocoderMetaData',
        'AddressDetails',
        'Country',
        'AdministrativeArea',
        'AdministrativeAreaName'
    ))
    name: str = Field(validation_alias=AliasPath('name'))
    latitude: str = Field(validation_alias=AliasPath('Point', 'pos'))
    longitude: str = Field(validation_alias=AliasPath('Point', 'pos'))


class WeatherSchema(BaseModel):
    temperature: float = Field(validation_alias=AliasPath('fact', 'temp'))
    feels_like: float = Field(validation_alias=AliasPath('fact', 'feels_like'))
    pressure: float = Field(validation_alias=AliasPath('fact', 'pressure_mm'))
    humidity: float = Field(validation_alias=AliasPath('fact', 'humidity'))
    wind_speed: float = Field(validation_alias=AliasPath('fact', 'wind_speed'))
    city: str = Field(validation_alias=AliasPath('geo_object', 'locality', 'name'))
