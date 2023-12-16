from typing import Mapping, Any

from pydantic import ValidationError

from app.utils.exceptions import WrongCity
from app.utils.logger import logger


async def validate_response_to_schema(schema: Any, response: Mapping[str, str]):
    try:
        convert_to_schema = schema.model_validate(response)
    except (IndexError, TypeError, KeyError, ValidationError) as error:
        logger.error(f'Ошибка при валидации данных. error: {error}')
        raise WrongCity

    return convert_to_schema
