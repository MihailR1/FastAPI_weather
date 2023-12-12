from fastapi import HTTPException, status


class BaseEx(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ConnectionToAPIError(BaseEx):
    status_code = status.HTTP_502_BAD_GATEWAY
    detail = 'Ошибка при обращении к внешнему API'


class WrongCity(BaseEx):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Пользователь ввел не существующий город'
