import asyncio
import logging

from aiogram import Dispatcher
from config import bot

dp = Dispatcher()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
                           '%(lineno)d - %(name)s - %(message)s'
                    )



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())