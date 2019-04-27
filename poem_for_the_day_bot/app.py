from aiohttp import web
from .urls import setup_routes


async def create_app():
    app = web.Application()
    setup_routes(app)
    return app
