from fastapi import FastAPI, Depends, Request, Response
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
        root_path="/api",
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

    @app.middleware("http")
    async def log_response(request: Request, call_next):
        response = await call_next(request)

        res_body = b""
        async for chunk in response.body_iterator:
            res_body += chunk
        logger.debug(res_body.decode())
        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    async def log_json(request: Request):
        logging.debug(await request.json())

    app.include_router(
        bill_app, tags=["Bills"], prefix="/bills", dependencies=[Depends(log_json)]
    )
    return app
