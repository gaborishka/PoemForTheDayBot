import os
from aiohttp import web
from .poem import get_poem_today


async def index(request):
    poem = await get_poem_today()
    return web.Response(text=poem)
