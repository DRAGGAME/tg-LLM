import asyncio

from aiogram import Dispatcher
from config import bot
from database.start_db import StartDB
from handlers.begin_handler import begin_router
from handlers.ml_handler import ml_handler
from handlers.settings_handlers import settings_router
# from logger import logger as logging

dp = Dispatcher()

dp.include_routers(begin_router, ml_handler, settings_router)



async def main():
    start_db = StartDB()
    await start_db.start_db()
    await start_db.connect()
    # print(await start_db.select_table())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())