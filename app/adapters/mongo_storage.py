import json
from bson import ObjectId, errors as bson_errors
from datetime import datetime
from pymongo import errors
from typing import Any, Dict, List

from app.usecases.ports.abstract_storage import AbstractStorage, Store

def bson_handler(data):
    if isinstance(data, datetime):
        return data.isoformat()

    if isinstance(data, ObjectId):
        return str(data)

    raise TypeError(data)


class MongoStorage(AbstractStorage):
    def __init__(self):
        super().__init__()

        self.__db = None

    def connect(self, client):
        try:
            self.__db = client.get_default_database()
        except errors.ConfigurationError:
            self.__db = client['db']

    def create(self, store: Store, objects: List[Dict[str, Any]]) -> int:
        collection = self.__db[store]

        created = 0

        if len(objects) > 1:
            result = collection.insert_many(objects)
            return len(result.inserted_ids)

        if len(objects) == 1:
            result = collection.insert_one(objects[0])
            created = 1 if isinstance(result.inserted_id, ObjectId) else 0

        return created

    def read(
        self,
        store: Store,
        filters: Dict[str, Any] = None,
        limit: int = 0,
        projection: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        filters = {} if filters is None else filters
        projection = {} if projection is None else projection

        items: List[Dict[str, Any]] = []

        try:
            result = self.__db[store].find(filters, projection=projection) \
                .limit(limit)
        except bson_errors.InvalidId as invalid_id:
            print(invalid_id)

        if result is None:
            return items

        items = [json.loads(json.dumps(r, default=bson_handler)) for r in result]

        return items
