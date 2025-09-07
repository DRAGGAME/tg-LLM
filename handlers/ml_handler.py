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

    if "short_description" in model:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, f"text{message.chat.id}.txt")

        with open(f"text{message.chat.id}.txt", "r") as file:
            text = ""
            for line in file:
                text += line
                response = await request_short_description(text)
        await message.answer(response)