from fastapi import APIRouter

from . import (
    get_horse,
)


def register_routers(app):
    router = APIRouter(prefix='/api/v1')
    router.include_router(
        router=get_horse.router,
    )
    app.include_router(router)
    return app
