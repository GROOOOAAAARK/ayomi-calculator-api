from abc import ABC, abstractmethod
from typing import Any
from app.usecases.response import Response

class Presenter(ABC):
    @abstractmethod
    def present(
        self,
        response: Response,
    ) -> Any:
        raise NotImplementedError
