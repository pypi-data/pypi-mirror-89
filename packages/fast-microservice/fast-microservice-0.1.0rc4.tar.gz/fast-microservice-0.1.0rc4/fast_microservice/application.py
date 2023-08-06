#!/usr/bin/env python

"""
inspiration.

* https://github.com/eightBEC/fastapi-ml-skeleton/tree/master/fastapi_skeleton
(APACHE 2.0)
* https://github.com/leosussan/fastapi-gino-arq-uvicorn
(PUBLIC DOMAIN)
"""

from fastapi import FastAPI

from fast_microservice.helpers import MiddlewareWrapper
from fast_microservice.routers import error, heartbeat, versions
from fast_microservice.settings.globals import (
    API_PREFIX,
    APP_NAME,
    APP_VERSION,
    DEBUG,
    SENTRY_DSN,
    SENTRY_ENABLED,
)

ROUTERS = (heartbeat.router, versions.router, error.router)


def get_app() -> FastAPI:
    """ Fastapi App instance. """
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=DEBUG)

    for router in ROUTERS:
        fast_app.include_router(router, prefix=API_PREFIX)

    if SENTRY_ENABLED and SENTRY_DSN not in ("None", ""):
        import sentry_sdk
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

        sentry_sdk.init(dsn=str(SENTRY_DSN))
        fast_app = MiddlewareWrapper(SentryAsgiMiddleware(fast_app))

    return fast_app


app = get_app()
