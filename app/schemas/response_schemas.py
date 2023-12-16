from pydantic import AliasChoices, AliasPath, BaseModel, Field, GetPydanticSchema
from pydantic_core import core_schema
from typing_extensions import Annotated


class CitySchema(BaseModel):
    country: str = Field(validation_alias=AliasPath(
        'metaDataProperty',
        'GeocoderMetaData',
        'AddressDetails',
        'Country',
        'CountryName'
    ))
    region: str = Field(validation_alias=AliasChoices(
        AliasPath(
            'metaDataProperty',
            'GeocoderMetaData',
            'AddressDetails',
            'Country',
            'AdministrativeArea',
            'AdministrativeAreaName'
        ),
        AliasPath('metaDataProperty',
                  'GeocoderMetaData',
                  'Address',
                  'formatted'
                  )
    ))
    name: str = Field(validation_alias=AliasPath('name'))
    latitude: Annotated[
        str,
        GetPydanticSchema(
            lambda tp, handler: core_schema.no_info_after_validator_function(
                lambda x: float(x.split()[1]), handler(tp)
            )
        ),
    ] = Field(validation_alias=AliasPath('Point', 'pos'))

    longitude: Annotated[
        str,
        GetPydanticSchema(
            lambda tp, handler: core_schema.no_info_after_validator_function(
                lambda x: float(x.split()[0]), handler(tp)
            )
        ),
    ] = Field(validation_alias=AliasPath('Point', 'pos'))


class WeatherSchema(BaseModel):
    temperature: float = Field(validation_alias=AliasPath('fact', 'temp'))
    feels_like: float = Field(validation_alias=AliasPath('fact', 'feels_like'))
    pressure: float = Field(validation_alias=AliasPath('fact', 'pressure_mm'))
    humidity: float = Field(validation_alias=AliasPath('fact', 'humidity'))
    wind_speed: float = Field(validation_alias=AliasPath('fact', 'wind_speed'))
    city: str = Field(validation_alias=AliasChoices(
        AliasPath('geo_object', 'locality', 'name'),
        AliasPath('geo_object', 'province', 'name')))
