from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceLevel, InlineChoiceFabric, QuestionLevelChoice, \
    InlineChoiceMode, InlineChoiceTextSettings

settings_router = Router(name="settings_router")
fabric_ml = InlineChoiceFabric()
sqlbase_request = UserQueries()


@settings_router.callback_query(InlineChoiceTextSettings.filter(F.mode_for_text == "level"))
async def edit_level_text(callback: CallbackQuery):
    """
    Клавиатура для изменения уровня вдумчивости
    :param callback:
    :return:
    """
    keyboard = await fabric_ml.change_question_data(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceTextSettings.filter(F.mode_for_text == "Questions"))
async def edit_question_level(callback: CallbackQuery):
    """
    Клавиатура для изменения уровня вопросов
    :param callback:
    :return:
    """
    keyboard = await fabric_ml.choice_question_level(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceLevel.filter(F.level.in_([1, 2, 3])))
async def change_level_text(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Уровни для вдумчивости
    :param callback:
    :param callback_data:
    :param state:
    :return:
    """
    try:
        keyboard = await fabric_ml.change_question_data(callback_data.level)

        level_detalisation = await state.get_value("question_level")

        if level_detalisation is None:
            level_detalisation = 1

        message_text = (f"Какие параметры вы будете использовать?\n\n"
                        f"Текущий уровень углублённости вопросов: {level_detalisation}\n"
                        f"Текущий уровень вдумчивости: {callback_data.level}\n")

        await callback.answer(f"Вдумчивость изменена на {callback_data.level}", show_alert=True)

        await callback.message.edit_text(message_text, reply_markup=keyboard)
        await state.update_data(level=callback_data.level)
    except TelegramBadRequest:
        await callback.answer("Уровень вдумчивости остался такой же...")


@settings_router.callback_query(QuestionLevelChoice.filter(F.question_level.in_([1, 2, 3])))
async def change_level_detalisation(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """
    Уровни для вопросов
    :param callback:
    :param callback_data:
    :param state:
    :return:
    """
    try:
        keyboard = await fabric_ml.choice_question_level(callback_data.question_level)
        await callback.message.edit_reply_markup(reply_markup=keyboard)

        level_detalisation = await state.get_value("level")

        if level_detalisation is None:
            level_detalisation = 1

        message_text = (f"Какие параметры вы будете использовать?\n\n"
                        f"Текущий уровень углублённости вопросов: {callback_data.question_level}\n"
                        f"Текущий уровень вдумчивости: {level_detalisation}\n")

        await callback.answer(f"Уровень детализации изменен на {callback_data.question_level}")
        await callback.message.edit_text(message_text, reply_markup=keyboard)

        await state.update_data(question_level=callback_data.question_level)
    except TelegramBadRequest:
        await callback.answer("Уровень углублённости вопросов остался такой же...")

@settings_router.callback_query(InlineChoiceMode.filter(F.mode))
async def answer_short_description(callback: CallbackQuery, callback_data: CallbackData):
    """
    Проверка на модели, будет обновлятся...
    :param callback:
    :param callback_data:
    """
    await sqlbase_request.connect()
    model = await sqlbase_request.get_user_model(str(callback.from_user.id))

    if callback_data.mode in model[0][0]:
        await callback.answer("Режим уже активирован")

    else:
        await sqlbase_request.update_model(str(callback.from_user.id), callback_data.mode)

    await sqlbase_request.close()


