from fastapi import HTTPException, status


class BaseEx(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoCityInDatabase(BaseEx):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Такого города нету в нашей базе данных'


class DataBaseError(BaseEx):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Ошибка при обращении к базе данных'


class ConnectionToAPIError(BaseEx):
    status_code = status.HTTP_502_BAD_GATEWAY
    detail = 'Ошибка при обращении к внешнему API'


class WrongCity(BaseEx):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Пользователь ввел не существующий город'
