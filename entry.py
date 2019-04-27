import aiohttp

from poem_for_the_day_bot import create_app

app = create_app()

if __name__ == '__main__':
    aiohttp.web.run_app(app, )