from aiofiles import os
from aiogram import Router, F
from aiogram.types import Message

from config import bot
from database.user_queries import UserQueries
from function.request_short_description import request_short_description
from handlers.begin_handler import sqlite

ml_handler = Router(name="ml_router")
sqlbase_request = UserQueries()

@ml_handler.message(F.document)
async def docx_handler(message: Message):
    await sqlbase_request.connect()
    print("test")
    model = await sqlbase_request.get_user_model(str(message.chat.id))

    if "short_description" == model[0][0]:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(file_path)
        await bot.download_file(file_path, f"{file_path.split('/')[-1]}")

        responses_list = await request_short_description(f"{file_path.split('/')[-1]}")

        await os.remove(f"{file_path.split('/')[-1]}")

        for response in responses_list:
            await message.answer(response)