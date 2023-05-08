import os

from fastapi import FastAPI
from . import config
from .dataBase.database import sessionmanager


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(os.getenv("DATABASE_URL"))

        def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                sessionmanager.close()

    server = FastAPI(title="abac-challenge", lifespan=lifespan)

    from fastapi.middleware.cors import CORSMiddleware

    from app.controller import user_router
    from app.controller import spaceship_router

    origins = ["*"]

    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    server.include_router(user_router, prefix="/api/user")
    server.include_router(spaceship_router, prefix="/api/spaceship")

    return server
