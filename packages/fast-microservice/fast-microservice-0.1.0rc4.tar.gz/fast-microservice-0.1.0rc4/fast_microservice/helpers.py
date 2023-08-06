def MiddlewareWrapper(middleware):
    """
    Wrap another Middleware ensure sane behaviour of the SentryAsgiMiddleware.

    According to issue:
    https://github.com/getsentry/sentry-python/issues/947

    The SentryAsgiMiddleware and Starlette 0.13 are incompatible with each other
    in early december 2020. From the thread we took a workaround to harness
    sentry into providing correct behaviour.
    """

    async def wrapper(*args, **kwds):
        return await middleware(*args, **kwds)

    return wrapper
