import asyncio
import logging

from aiogram import Dispatcher
from config import bot
from database.start_db import StartDB
from handlers.begin_handler import begin_router
from handlers.ml_handler import ml_handler

dp = Dispatcher()

dp.include_routers(begin_router, ml_handler)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
                           '%(lineno)d - %(name)s - %(message)s'
                    )



async def main():
    start_db = StartDB()
    await start_db.start_db()
    await start_db.connect()
    print(await start_db.select_table())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())