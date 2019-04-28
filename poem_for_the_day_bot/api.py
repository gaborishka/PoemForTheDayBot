from aiohttp import web
import os


async def index(request):
    return web.Response(text=os.environ['MESSAGE'])
