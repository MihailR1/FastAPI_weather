from typing import Mapping, TypeVar, Generic, Any

import pydantic
from pydantic import ValidationError

from app.utils.exceptions import ValidationSchemaError
from app.utils.logger import logger


_SchemaType = TypeVar('_SchemaType', bound=pydantic.BaseModel)


async def validate_response_to_schema(
        schema: Generic[_SchemaType], response: Mapping[str, Any]) -> _SchemaType:

    try:
        convert_to_schema = schema.model_validate(response)
    except ValidationError as error:
        logger.error(f'Ошибка при валидации данных. error: {error}')
        raise ValidationSchemaError

    return convert_to_schema
