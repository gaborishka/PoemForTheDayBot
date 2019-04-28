from aiohttp import web
from .urls import setup_routes
from .db import init_pg, close_pg


async def create_app():
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    return app
