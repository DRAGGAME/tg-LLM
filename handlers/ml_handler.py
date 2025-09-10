from aiofiles import os
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from config import bot
from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceFabric, InlineChoiceSettings
from function.request_short_description import request_short_description
from handlers.begin_handler import sqlite

ml_handler = Router(name="ml_router")
sqlbase_request = UserQueries()
fabric_ml = InlineChoiceFabric()

class DocumentHandler(StatesGroup):
    document_setting = State()


@ml_handler.message(F.document)
async def docx_handler(message: Message, state: FSMContext):
    await sqlbase_request.connect()
    user_model = await sqlbase_request.get_user_model(str(message.chat.id))
    keyboard_a_documents = await fabric_ml.choice_settings_text(user_model[0][0])
    await sqlbase_request.close()
    file_id = message.document.file_id
    await state.update_data(new_file_id=file_id)
    await message.answer(text="Какие параметры вы будете использовать?\n\n"
                              f"Текущая модель: {user_model[0][0]}\n"
                              f"Текущий уровень углублённости вопросов: 1(лёгкий)\n"
                              f"Текущий уровень количества вопросов: 1(маленький)\n", reply_markup=keyboard_a_documents)

@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action=="run"))
async def docx_handler_run(callback: CallbackQuery, state: FSMContext):

    await sqlbase_request.connect()
    print("test")
    model = await sqlbase_request.get_user_model(str(callback.message.chat.id))

    if "short_description" == model[0][0]:
        file_id = await state.get_value("new_file_id")
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(file_path)
        await bot.download_file(file_path, f"{file_path.split('/')[-1]}")
        await callback.answer("Обработка файла...")
        responses_list = await request_short_description(f"{file_path.split('/')[-1]}")

        await os.remove(f"{file_path.split('/')[-1]}")

        for response in responses_list:
            await callback.message.answer(response)
