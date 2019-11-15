from aiohttp import web

from views import handle, sync


def init_routes(app):
    app.add_routes([web.get('/', handle),
                    web.get('/sync/', sync),
                    web.get('/{name}', handle)])
