import os
from typing import Dict, Type
from dependency_injector import containers
from pydantic_settings import BaseSettings
from pymongo import MongoClient

from app import usecases
from app.infrastructure.dependency_injection_container import MainContainer, TestContainer

class Settings(BaseSettings):
    app_env: str = ''
    storage_uri: str = ''
    Container: Type[containers.DeclarativeContainer] = MainContainer

class TestSettings(Settings):
    app_env: str = 'test'
    Container: Type[containers.DeclarativeContainer] = TestContainer

class DevSettings(Settings):
    app_env: str = 'prod'
    debug: bool = False
    logging_level: str = 'info'

def configure_dependency_injection(configs: Dict[str, Settings], env: str):
    container = configs[env].Container()

    mongodb_client = MongoClient(
        host=configs[env].storage_uri,
        authSource='admin',
        connect=True,
    )
    container.storage().connect(client=mongodb_client)

    container.wire(packages=[usecases])

def get_config(env: str = ''):
    current_path = os.path.dirname(__file__)
    os.chdir(f'{current_path}/..')

    app_configs = {
        'test': TestSettings(),
        'dev': DevSettings(),
    }

    if env == '' or env not in app_configs:
        env = os.getenv('ENV', 'dev')

    configure_dependency_injection(app_configs, env)

    return app_configs[env]
