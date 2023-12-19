from pydantic import AliasChoices, AliasPath, BaseModel, Field, computed_field


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
    geo_position: str = Field(exclude=True, validation_alias=AliasPath('Point', 'pos'))

    @computed_field
    @property
    def latitude(self) -> float:
        return float(self.geo_position.split()[1])

    @computed_field
    @property
    def longitude(self) -> float:
        return float(self.geo_position.split()[0])


class WeatherSchema(BaseModel):
    temperature: float = Field(validation_alias=AliasPath('fact', 'temp'))
    feels_like: float = Field(validation_alias=AliasPath('fact', 'feels_like'))
    pressure: float = Field(validation_alias=AliasPath('fact', 'pressure_mm'))
    humidity: float = Field(validation_alias=AliasPath('fact', 'humidity'))
    wind_speed: float = Field(validation_alias=AliasPath('fact', 'wind_speed'))
    city: str = Field(validation_alias=AliasChoices(
        AliasPath('geo_object', 'locality', 'name'),
        AliasPath('geo_object', 'province', 'name')))
