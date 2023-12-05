from abc import abstractmethod
from typing import Any, Dict, List, Literal

from app.usecases.ports.meta_singleton import MetaSingleton

Store = Literal[
    '_dummy_',
    'calculations',
]

class AbstractStorage(metaclass=MetaSingleton):

    @abstractmethod
    def connect(self, client):
        raise NotImplementedError

    @abstractmethod
    def create(self, store: Store, objects: List[Dict[str, Any]]) -> int:
        raise NotImplementedError

    @abstractmethod
    def read(self, store: Store, filters: Dict[str, Any] = None, limit: int = 0,) -> List[Dict]:
        raise NotImplementedError
