from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceSize, InlineChoiceFabric, QuestionLevelChoice, \
    InlineChoiceMode, InlineChoiceTextSettings

settings_router = Router(name="settings_router")
fabric_ml = InlineChoiceFabric()
sqlbase_request = UserQueries()


@settings_router.callback_query(InlineChoiceTextSettings.filter(F.mode_for_text == "size"))
async def edit_size_text(callback: CallbackQuery):
    await sqlbase_request.connect()
    last_mode = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()
    keyboard = await fabric_ml.choice_size_text(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceTextSettings.filter(F.mode_for_text == "Questions"))
async def edit_question_level(callback: CallbackQuery):
    await sqlbase_request.connect()
    last_mode = await sqlbase_request.get_user_model(str(callback.from_user.id))
    await sqlbase_request.close()
    keyboard = await fabric_ml.choice_question_level(1)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@settings_router.callback_query(InlineChoiceSize.filter(F.size_text.in_([1, 2, 3])))
async def change_size_text(callback: CallbackQuery, callback_data: CallbackData):
    if callback_data.size_text == 1:
        keyboard = await fabric_ml.choice_size_text(1)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Размер текста изменен на 1")
    elif callback_data.size_text == 2:
        keyboard = await fabric_ml.choice_size_text(2)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Размер текста изменен на 2")
    elif callback_data.size_text == 3:
        keyboard = await fabric_ml.choice_size_text(3)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        await callback.answer("Размер текста изменен на 3")


@settings_router.callback_query(QuestionLevelChoice.filter(F.question_level.in_([1, 2, 3])))
async def change_level_detalisation(callback: CallbackQuery, callback_data: CallbackData):
    try:
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
    except TelegramBadRequest:
        await callback.answer("Уровень ")
