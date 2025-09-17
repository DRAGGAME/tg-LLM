from aiofiles import os
from aiogram import Router, F, flags
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from config import bot
from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceFabric, InlineChoiceSettings
from function.request_short_description import request_short_description
from logger import logger

ml_handler = Router(name="ml_router")
sqlbase_request = UserQueries()
fabric_ml = InlineChoiceFabric()


class DocumentHandler(StatesGroup):
    document_setting = State()


@ml_handler.message(F.document)
async def docx_handler(message: Message, state: FSMContext):
    await sqlbase_request.connect()
    user_model = await sqlbase_request.get_user_model(str(message.chat.id))
    keyboard_a_documents = await fabric_ml.choice_fabric()
    await sqlbase_request.close()

    file_id = message.document.file_id
    await state.update_data(new_file_id=file_id)

    await message.answer(text="Какие параметры вы будете использовать?\n\n"
                              f"Текущий уровень углублённости вопросов: 1\n"
                              f"Текущий уровень детализации: 1\n", reply_markup=keyboard_a_documents)


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "settings"))
async def settings_handler(callback: CallbackQuery):
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()
    kb = await fabric_ml.choice_mode(model)

    await callback.message.edit_text("Выберите режим работы", reply_markup=kb)
    await callback.answer()


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "settings_text"))
async def settings_text_handler(callback: CallbackQuery):
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()
    kb = await fabric_ml.choice_settings_text(model[0][0])
    await callback.message.edit_text("Выберите, что вы хотите настроить", reply_markup=kb)
    await callback.answer()


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "run"))
@flags.chat_action("typing")
async def docx_handler_run(callback: CallbackQuery, state: FSMContext):
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.message.chat.id))
    if "short_description" == model[0][0]:

        file_id = await state.get_value("new_file_id")
        file = await bot.get_file(file_id)
        file_path = file.file_path

        level_size = await state.get_value("size_text")
        question_level = await state.get_value("question_level")

        if bool(level_size) is False:
            level_size = 1

        if bool(question_level) is False:
            question_level = 1


        await bot.download_file(file_path, f"{file_path.split('/')[-1]}")
        await callback.message.delete()
        await callback.answer("Обработка файла...")

        responses_list = await request_short_description(f"{file_path.split('/')[-1]}", int(level_size),
                                                         int(question_level))

        await os.remove(f"{file_path.split('/')[-1]}")
        for response in responses_list:
            await callback.message.answer(response)

        await state.clear()
