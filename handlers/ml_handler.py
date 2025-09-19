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
    """
    Хэндлер для принятия документа
    :param message:
    :param state:
    :return:
    """
    await state.clear()

    file_id = message.document.file_id
    await state.update_data(new_file_id=file_id)

    keyboard_a_documents = await fabric_ml.choice_fabric()
    logger.info(f"Пользователь с user_id({message.from_user.id}) и ником({message.from_user.username}) отправил файл")

    await message.answer(text="Какие параметры вы будете использовать?\n\n"
                              f"Текущий уровень углублённости вопросов: 1\n"
                              f"Текущий уровень детализации: 1\n", reply_markup=keyboard_a_documents)


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "settings"))
async def settings_handler(callback: CallbackQuery):
    """
    Выбор режима работы
    :param callback:
    :return:
    """
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()

    kb = await fabric_ml.choice_mode(model)

    await callback.message.edit_text("Выберите режим работы", reply_markup=kb)
    await callback.answer()


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "settings_text"))
async def settings_text_handler(callback: CallbackQuery, state: FSMContext):
    """
    Настройки работы
    :param callback:
    :param state:
    :return:
    """
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()

    level = await state.get_value("level")
    level_question = await state.get_value("question_level")

    if not level:
        level = 1
        await state.update_data(level=level)

    if not level_question:
        level_question = 1
        await state.update_data(question_level=level_question)

    message_text = ("Какие параметры вы будете использовать?\n\n"
                  f"Текущий уровень углублённости вопросов: {level_question}\n"
                  f"Текущий уровень детализации: {level}")

    kb = await fabric_ml.choice_settings_text(model[0][0])

    await callback.message.edit_text(f"{message_text}", reply_markup=kb)
    await callback.answer()


@ml_handler.callback_query(InlineChoiceSettings.filter(F.setting_action == "run"))
async def docx_handler_run(callback: CallbackQuery, state: FSMContext):
    """
    Запуск обработки через ИИ файла
    :param callback:
    :param state:
    :return:
    """

    for _ in range(0, 2):
        try:
            await sqlbase_request.connect()
            model = await sqlbase_request.get_user_model(str(callback.message.chat.id))
            await sqlbase_request.close()
            if "short_description" == model[0][0]:
                print("yes")
                # Краткое описание
                file_id = await state.get_value("new_file_id")

                file = await bot.get_file(file_id)
                file_path = file.file_path

                level = await state.get_value("level")
                question_level = await state.get_value("question_level")

                if not bool(level):
                    level = 1

                if not bool(question_level):
                    question_level = 1

                await bot.download_file(file_path, f"{file_path.split('/')[-1]}")

                logger.info(
                    f"Пользователь с user_id({callback.message.from_user.id}) ) был отправлен запрос к ИИ с данными:"
                    f"Вдумчивость: {level}\nВопрсы: {question_level}")

                await callback.message.delete()
                await callback.answer("Обработка файла...")

                responses_list = await request_short_description(f"{file_path.split('/')[-1]}", int(level),
                                                                 int(question_level))

                await os.remove(f"{file_path.split('/')[-1]}")
                for response in responses_list:
                    await callback.message.answer(response)
                    logger.info(f"Пользователь с user_id({callback.message.from_user.id}) )"
                                f"Отправлено сообщение")
                logger.info(f"Пользователь с user_id({callback.message.from_user.id}))\n"
                            f"Закончена отправка сообщений")
                await state.clear()
                break
        except IndexError:
            await sqlbase_request.connect()
            print("test")
            logger.info(
                f"Пользователь с user_id({callback.message.from_user.id}) ) обновил и запустил бота")
            user_id = callback.message.from_user.id
            username = callback.message.from_user.username

            data = await sqlbase_request.get_user_model(str(user_id))
            if not data:
                await sqlbase_request.insert_user(username, str(user_id))

            await sqlbase_request.close()

            continue