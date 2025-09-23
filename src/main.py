from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from src.admin import register_admin_views
from src.authentication.views import router as auth_router
from src.base_settings import base_settings
from src.catalogue.utils import ProductElasticManager
from src.catalogue.views import product_router, category_router
from src.common.databases.postgres import (
    engine,
    init_db,
)
from src.general.views import router as status_router
from src.routes import BaseRoutesPrefixes
from src.users.views import user_router


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa: ARG001
    await init_db()
    await ProductElasticManager().init_indices()

    yield


def include_routes(application: FastAPI) -> None:
    application.include_router(
        router=status_router,
    )
    application.include_router(
        router=auth_router,
        prefix=BaseRoutesPrefixes.authentication,
        tags=['Authentication'],
    )
    application.include_router(
        router=product_router,
        prefix=BaseRoutesPrefixes.catalogue,
        tags=['Catalogue'],
    )
    application.include_router(
        router=user_router,
        prefix=BaseRoutesPrefixes.account,
        tags=['Account'],
    )
    application.include_router(
        router=category_router,
        prefix=BaseRoutesPrefixes.catalogue,
        tags=['Categories'],
    )


def get_application() -> FastAPI:
    application = FastAPI(
        debug=base_settings.debug,
        docs_url=BaseRoutesPrefixes.swagger if base_settings.debug else None,
        redoc_url=BaseRoutesPrefixes.redoc if base_settings.debug else None,
        openapi_url=BaseRoutesPrefixes.openapi if base_settings.debug else None,
        lifespan=lifespan,
    )

    admin = Admin(app=application, engine=engine)
    register_admin_views(admin)

    include_routes(application)

    return application


app = get_application()
