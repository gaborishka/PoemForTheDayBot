import aiohttp

from poem_for_the_day import create_app

app = create_app()

if __name__ == '__main__':
    aiohttp.web.run_app(app, )