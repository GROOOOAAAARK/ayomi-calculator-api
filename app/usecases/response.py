from enum import Enum
from typing import Optional, Dict, Any

class ResponseMessage(str, Enum):
    EXPRESSION_EVALUATED = 'Expression evaluated'
    INVALID_EXPRESSION = 'Invalid expression'
    DIVISION_BY_ZERO = 'Division by zero'
    NO_CALCULATIONS = 'No calculations'

    def __str__(self) -> str:
        return str(self.value)

class ResponseStatus(str, Enum):
    OK = 'OK'
    CREATED = 'Created'
    ACCEPTED = 'Accepted'
    BADREQUEST = 'BadRequest'
    NOTFOUND = 'NotFound'
    TEAPOT = 'I\'mATeapot'

    def __str__(self) -> str:
        return str(self.value)


class Response:
    def __init__(
        self,
        success: bool,
        status: ResponseStatus,
        message: Optional[ResponseMessage],
        data: Optional[Dict[str, Any] | str]
    ) -> None:
        self.__success = success
        self.__status = status
        self.__message = message
        self.__data = data

    @property
    def status(self) -> ResponseStatus:
        return self.__status

    @property
    def message(self) -> Optional[str]:
        return self.__message if self.__message is not None else None

    @property
    def data(self) -> Optional[Dict[str, Any]] | str:
        return self.__data.copy() if self.__data is not None \
            and isinstance(self.__data, Dict) else self.__data


    @classmethod
    def succeeded(
        cls,
        status: ResponseStatus = ResponseStatus.OK,
        message: Optional[ResponseMessage] = None,
        data: Optional[Dict[str, Any] | str] = None,
    ) -> 'Response':
        return cls(
            True,
            status,
            message,
            data,
        )

    @classmethod
    def failed(
        cls,
        status: ResponseStatus = ResponseStatus.TEAPOT,
        message: Optional[ResponseMessage] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> 'Response':
        return cls(
            False,
            status,
            message,
            data,
        )
