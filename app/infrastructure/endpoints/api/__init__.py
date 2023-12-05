from fastapi import FastAPI

from app.infrastructure.endpoints.api.calculation import router as calculation
from app.infrastructure.configs import Settings, get_config
from fastapi.middleware.cors import CORSMiddleware

def get_app(config: Settings = None): #type: ignore
    if config is None:
        config = get_config('dev')

    app = FastAPI(
        title="FastAPI Template",
        debug=config.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(calculation)

    return app
