import aiohttp
from bs4 import BeautifulSoup
import datetime
import asyncio

loop = asyncio.get_event_loop()


async def get_poem_today():
    data = datetime.date.today()
    url = f'https://wol.jw.org/ru/wol/dt/r2/lp-u/{data.year}/{data.month}/{data.day}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")

            title = soup.find('div', {'class': 'todayItems'}).find('h2').text
            poem = soup.find('p', {'class': 'themeScrp'}).text
            text = soup.find('p', {'class': 'sb'}).text

            poem_day = f'''<em>{title}</em>\n<b>{poem}</b>\n{text}'''

            return poem_day


if __name__ == '__main__':
    print(loop.run_until_complete(get_poem_today()))
