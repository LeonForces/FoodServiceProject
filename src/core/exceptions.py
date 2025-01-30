from fastapi import HTTPException, status


class AutoException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CredentialsException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не удалось проверить учетные данные"


class LoginException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class UserAlreadyExistsException(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"
