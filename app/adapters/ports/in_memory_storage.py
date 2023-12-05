from typing import Any, Dict, List
from app.usecases.ports.abstract_storage import AbstractStorage, Store

class InMemoryStorage(AbstractStorage):

    def __init__(self):
        super().__init__()

        # initialize database with provided data
        self.stores: dict[Store, list] = {
            'dummy': [],
            'calculations': [],
        }

    def connect(self, client):
        pass

    def create(self, store: Store, objects: List[Dict]) -> int:
        created = 0

        try:
            self.stores[store].extend(objects)
            created += len(objects)
        except KeyError as key_error:
            print(key_error)

        return created

    def read(
        self,
        store: Store,
        filters: dict[str, Any],
        limit: int = 0,
        projection: dict[str, Any] = None,
    ) -> list[Dict]:
        return [
            item
            for item in self.stores[store]
        ]
