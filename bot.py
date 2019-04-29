import asyncio
import os
import logging
import datetime


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from poem_for_the_day.poem import get_poem_today
from aiogram.types import ParseMode
from poem_for_the_day.db import init_pg, close_pg, get_user
from poem_for_the_day.db import users

bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(bot)

db = dict()
loop = asyncio.get_event_loop()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    data = {
        'id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'time': None
    }

    await add_user(data)

    await message.reply("Привет!\nЯ буду каждый день присылать тебе ежедневный стих. Со мной ты точно не забудешь "
                        "его прочитать")
    mes = await get_poem_today()
    await bot.send_message(message.from_user.id, mes, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Все, что я сейчас умею делать, это напоминать тебе прочитать ежедневный стих. Тебе для "
                        "этого ничего не нужно делать, просто активируй меня командой '/start' и каждый день я буду "
                        "честно выполнять свою роботу")


@dp.message_handler(commands=['poem'])
async def echo_message(msg: types.Message):
    mes = await get_poem_today()
    await bot.send_message(msg.from_user.id, mes, parse_mode=ParseMode.HTML)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Извини, я пока что не понимаю этот странный язык. Я просто делаю "
                                             "ежедневную рассылку.")


async def add_user(data):
    async with db['db'].acquire() as conn:
        try:
            exist = await get_user(conn, data['id'])
            if not exist:
                await conn.execute(users.insert(), [data])
        except Exception as e:
            logging.error(str(e))
            raise e


if __name__ == '__main__':

    today = str(datetime.date.today())
    logging.basicConfig(level=logging.ERROR, format="%(message)s", filename='./logs/logging-{}.txt'.format(today))

    loop.run_until_complete(init_pg(db))

    executor.start_polling(dp)

    loop.run_until_complete(close_pg(db))
