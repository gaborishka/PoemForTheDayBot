from . import api


def setup_routes(app):
    router = app.router

    router.add_route('GET', '/', api.index)
