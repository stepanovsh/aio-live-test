import logging
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from routes import init_routes


def init_app(argv=None) -> web.Application:
    app = web.Application()
    init_routes(app)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(dir_path, 'templates')))

    return app


app = init_app()

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    web.run_app(app)
