import logging
from aiohttp import web

from routes import init_routes


def init_app(argv=None) -> web.Application:
    app = web.Application()
    init_routes(app)
    return app


app = init_app()

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    web.run_app(app)
