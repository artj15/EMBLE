from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from models.base import (
    ValidationError,
    ErrorResponse,
)


async def error_500(detail: str = None, debug: str = None) -> JSONResponse:
    return JSONResponse(status_code=500,
                        content=ErrorResponse(error=detail or 'Server internal fatal_error', debug=debug).dict())


async def error_404(message: str = None) -> JSONResponse:
    return JSONResponse(status_code=404, content=ErrorResponse(error=message or 'not found').dict())


async def error_400(message: str = None) -> JSONResponse:
    return JSONResponse(status_code=400, content=ErrorResponse(error=message or 'invalid input data').dict())


def register_exception_handler(app):
    if not app.config['debug']:
        @app.exception_handler(Exception)
        async def http_exception_handler(request, exc) -> JSONResponse:
            return await error_500(debug=str(exc) if app.config['debug'] else None)

        @app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request, exc) -> JSONResponse:
            return await error_500(debug=str(exc) if app.config['debug'] else None)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        validation_error = None
        errors = exc.errors()
        if errors:
            validation_error = []
            for i in errors:
                validation_error.append(
                    ValidationError(
                        field='.'.join([str(l) for l in i['loc'][1:]]),
                        message=i['msg']
                    )
                )
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error='Client sent incomplete data',
                validation_error=validation_error,
                debug=str(exc) if app.config['debug'] else None
            ).dict())
