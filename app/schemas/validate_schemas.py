from typing import Mapping

import pydantic
from pydantic import ValidationError

from app.utils.exceptions import ValidationSchemaError
from app.utils.logger import logger


async def validate_response_to_schema(schema: pydantic.BaseModel, response: Mapping[str, str]) -> pydantic.BaseModel:
    try:
        convert_to_schema = schema.model_validate(response)
    except ValidationError as error:
        logger.error(f'Ошибка при валидации данных. error: {error}')
        raise ValidationSchemaError

    return convert_to_schema
