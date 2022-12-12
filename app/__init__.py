from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

import logging

from .config import Settings

logger = logging.getLogger(__name__)


def create_app(config: Settings) -> FastAPI:
    from .routes.bill import bill as bill_app

    def custom_generate_unique_id(route: APIRoute):
        return route.name

    app = FastAPI(
        generate_unique_id_function=custom_generate_unique_id,
        docs_url="/docs",
        redoc_url="/redoc",
        root_path="/",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup_db_client():
        app.mongodb_client = MongoClient(config.atlas_uri)
        app.database = app.mongodb_client[config.db_name]

    @app.on_event("shutdown")
    def shutdown_db_client():
        app.mongodb_client.close()

    app.include_router(
        bill_app,
        tags=["Bills"],
        prefix="/bills",
    )
    return app
