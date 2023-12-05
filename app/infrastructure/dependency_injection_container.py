from dependency_injector import containers, providers

from app.adapters.mongo_storage import MongoStorage
from app.adapters.ports.in_memory_storage import InMemoryStorage


class MainContainer(containers.DeclarativeContainer):

    storage = providers.Singleton(MongoStorage)

class TestContainer(containers.DeclarativeContainer):

    storage = providers.Singleton(InMemoryStorage)
