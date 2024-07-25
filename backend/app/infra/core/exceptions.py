# Base source: https://github.com/polarsource/polar/blob/main/server/polar/kit/db/models/base.py

from typing import Any, Literal, LiteralString, TypedDict

from pydantic import BaseModel, create_model
from pydantic_core import ErrorDetails, InitErrorDetails, PydanticCustomError
from pydantic_core import ValidationError as PydanticValidationError

from app.infra.config import settings


class ProdkitError(Exception):
    """
    Base exception class for all errors raised by Prodkit.

    A custom exception handler for FastAPI takes care
    of catching and returning a proper HTTP error from them.

    Args:
        message: The error message that'll be displayed to the user.
        status_code: The status code of the HTTP response. Defaults to 500.
        headers: Additional headers to be included in the response.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

    @classmethod
    def schema(cls) -> type[BaseModel]:
        type_literal = Literal[cls.__name__]  # type: ignore

        return create_model(cls.__name__, type=(type_literal, ...), detail=(str, ...))


class ProdkitTaskError(ProdkitError):
    """
    Base exception class for errors raised by tasks.

    Args:
        message: The error message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ProdkitRedirectionError(ProdkitError):
    """
    Exception class for errors
    that should be displayed nicely to the user through our UI.

    A specific exception handler will redirect to `/error` page in the client app.

    Args:
        return_to: Target URL of the *Go back* button on the error page.
    """

    def __init__(
        self, message: str, status_code: int = 400, return_to: str | None = None
    ) -> None:
        self.return_to = return_to
        super().__init__(message, status_code)


class BadRequestError(ProdkitError):
    def __init__(self, message: str = "Bad request", status_code: int = 400) -> None:
        super().__init__(message, status_code)


class NotPermittedError(ProdkitError):
    def __init__(self, message: str = "Not permitted", status_code: int = 403) -> None:
        super().__init__(message, status_code)


class UnauthorizedError(ProdkitError):
    def __init__(self, message: str = "Unauthorized", status_code: int = 401) -> None:
        super().__init__(
            message,
            status_code,
            headers={
                "WWW-Authenticate": f'Bearer realm="{settings.WWW_AUTHENTICATE_REALM}"'
            },
        )


class InternalServerError(ProdkitError):
    def __init__(
        self, message: str = "Internal Server Error", status_code: int = 500
    ) -> None:
        super().__init__(message, status_code)


class ResourceNotFoundError(ProdkitError):
    def __init__(self, message: str = "Not found", status_code: int = 404) -> None:
        super().__init__(message, status_code)


class ResourceUnavailableError(ProdkitError):
    def __init__(self, message: str = "Unavailable", status_code: int = 410) -> None:
        super().__init__(message, status_code)


class ResourceAlreadyExistsError(ProdkitError):
    def __init__(self, message: str = "Already exists", status_code: int = 409) -> None:
        super().__init__(message, status_code)


class ValidationError(TypedDict):
    loc: tuple[int | str, ...]
    msg: LiteralString
    type: LiteralString
    input: Any


class ProdkitRequestValidationError(ProdkitError):
    def __init__(self, errors: list[ValidationError]) -> None:
        self._errors = errors

    def errors(self) -> list[ErrorDetails]:
        pydantic_errors: list[InitErrorDetails] = []
        for error in self._errors:
            pydantic_errors.append(
                {
                    "type": PydanticCustomError(error["type"], error["msg"]),
                    "loc": error["loc"],
                    "input": error["input"],
                }
            )
        pydantic_error = PydanticValidationError.from_exception_data(
            self.__class__.__name__, pydantic_errors
        )
        return pydantic_error.errors()


class PasswordNotValidError(Exception):
    def __init__(self, password: str, message: str = "Password is not valid"):
        self.password = password
        self.message = message
        super().__init__(self.message)


class PhoneNotValidError(Exception):
    def __init__(self, phone: str, message: str = "Phone number is not valid"):
        self.phone = phone
        self.message = message
        super().__init__(self.message)


class MissingTenantOrAccountIdError(ProdkitError):
    def __init__(
        self,
        message: str = "Tenant ID and Account ID are required",
        status_code: int = 400,
    ) -> None:
        super().__init__(message, status_code)
