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
async def edit_size_text(callback: CallbackQuery):
    await sqlbase_request.connect()
    last_mode = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()
    keyboard = await fabric_ml.change_question_data(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceTextSettings.filter(F.mode_for_text == "Questions"))
async def edit_question_level(callback: CallbackQuery):
    keyboard = await fabric_ml.choice_question_level(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceLevel.filter(F.level.in_([1, 2, 3])))
async def change_size_text(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    try:
        keyboard = await fabric_ml.change_question_data(1)
        if callback_data.level == 1:
            keyboard = await fabric_ml.change_question_data(1)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Вдумчивость изменена на 1", show_alert=True)
        elif callback_data.level == 2:
            keyboard = await fabric_ml.change_question_data(2)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Вдумчивость изменена на 2", show_alert=True)
        elif callback_data.level == 3:
            keyboard = await fabric_ml.change_question_data(3)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Вдумчивость изменена на 3", show_alert=True)

        level_detalisation = await state.get_value("level_detalisation")

        if bool(level_detalisation) is False:
            level_detalisation = 1

        message_text = (f"Какие параметры вы будете использовать?\n\n"
                      f"Текущий уровень углублённости вопросов: {level_detalisation}\n"
                      f"Текущий уровень детализации: {callback_data.level}\n")

        await callback.message.edit_text(message_text, reply_markup=keyboard)
        await state.update_data(question_data=callback_data.size_text)
    except TelegramBadRequest:
        await callback.answer("Уровень углублённости вопросов остался такой же...")

@settings_router.callback_query(QuestionLevelChoice.filter(F.question_level.in_([1, 2, 3])))
async def change_level_detalisation(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    try:
        keyboard = await fabric_ml.choice_question_level(1)

        if callback_data.question_level == 1:
            keyboard = await fabric_ml.choice_question_level(1)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Уровень детализации изменен на 1")

        elif callback_data.question_level == 2:
            keyboard = await fabric_ml.choice_question_level(2)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Уровень детализации изменен на 2")

        elif callback_data.question_level == 3:
            keyboard = await fabric_ml.choice_question_level(3)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer("Уровень детализации изменен на 3")

        level_detalisation = await state.get_value("level_detalisation")

        if bool(level_detalisation) is False:
            level_detalisation = 1

        message_text = (f"Какие параметры вы будете использовать?\n\n"
                      f"Текущий уровень углублённости вопросов: {level_detalisation}\n"
                      f"Текущий уровень детализации: {callback_data.question_level}\n")

        await callback.message.edit_text(message_text, reply_markup=keyboard)

        await state.update_data(question_level=callback_data.question_level)
    except TelegramBadRequest:
        await callback.answer("Уровень детализации остался такой же...")
