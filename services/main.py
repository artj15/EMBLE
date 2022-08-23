import logging

from fastapi import (
    FastAPI,
)

from misc import (
    db,
    ctrl,
)
from misc.handlers import register_exception_handler
from models.base import ErrorResponse, UpdateErrorResponse

logger = logging.getLogger(__name__)


def factory():
    app = ctrl.main_with_parses(main)
    if not app:
        raise RuntimeError
    return app


def main(config):
    root_path = config.get('rot_path', None)
    app = FastAPI(
        title='Fastapi template REST API',
        debug=config.get('debug', False),
        root_path=root_path,
        responses=responses(),
    )
    app.config = config
    register_exception_handler(app)
    register_routers(app)
    register_startup(app)
    register_shutdown(app)

    return app


def register_startup(app):
    @app.on_event("startup")
    async def handler_startup():
        logger.info('Startup called')
        try:
            await startup(app)
            logger.info(f"REST API app startup executed")
        except:
            logger.exception('Startup crashed')


def register_shutdown(app):
    @app.on_event("shutdown")
    async def handler_shutdown():
        logger.info('Shutdown called')
        try:
            await shutdown(app)
            logger.info(f"REST API app shutdown executed")
        except:
            logger.exception('Shutdown crashed')


async def startup(app):
    app.db_pool = await db.init(app.config['db'])
    return app


async def shutdown(app):
    if app.db_pool:
        await app.db_pool.close()


def register_routers(app):
    from . import routers
    return routers.register_routers(app)


def responses():
    return {
        409: {
            "model": UpdateErrorResponse
        },
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
