import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from poem_for_the_day_bot.db import init_pg, close_pg
from poem_for_the_day_bot.db import get_users as all_users
from poem_for_the_day_bot.poem import get_poem_today

API_TOKEN = os.environ['TOKEN']

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop)

db = dict()


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def send_message(user_id: int, text: str) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param text:
    :return:
    """

    poem_message = await get_poem_today()
    try:

        await bot.send_message(user_id, poem_message)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    """
    Simple broadcaster

    :return: Count of messages
    """
    count = 0
    await init_pg(db)

    async with db['db'].acquire() as conn:
        data = await all_users(conn)

        try:
            for user in data:
                if await send_message(user['id'], '<b>Hello!</b>'):
                    count += 1
                await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        finally:
            log.info(f"{count} messages successful sent.")
            await close_pg(db)

        return count


if __name__ == '__main__':
    # Execute broadcaster
    executor.start(dp, broadcaster())
