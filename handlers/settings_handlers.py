from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from fabric_keyboard.inline_choice_fabric import InlineChoiceSize, InlineChoiceFabric, QuestionLevelChoice

settings_router = Router(name="settings_router")
fabric_ml = InlineChoiceFabric()

@settings_router.callback_query(InlineChoiceSize.filter(F.size_text.in_([1, 2, 3])))
async def change_size_text(callback: CallbackQuery, callback_data: CallbackData):
    if callback_data.size_text == 1:
        await fabric_ml.choice_size_text(1)
        await callback.answer("Размер текста изменен на 1")
    elif callback_data.size_text == 2:
        await fabric_ml.choice_size_text(2)
        await callback.answer("Размер текста изменен на 2")
    elif callback_data.size_text == 3:
        await fabric_ml.choice_size_text(3)
        await callback.answer("Размер текста изменен на 3")

@settings_router.callback_query(QuestionLevelChoice.filter(F.question_level.in_([1, 2, 3])))
async def change_level_detalisation(callback: CallbackQuery, callback_data: CallbackData):
    if callback_data.size_text == 1:
        await fabric_ml.choice_question_level(1)
        await callback.answer("Уровень детализации изменен на 1")

    elif callback_data.size_text == 2:
        await fabric_ml.choice_question_level(2)
        await callback.answer("Уровень детализации изменен на 2")

    elif callback_data.size_text == 3:
        await fabric_ml.choice_question_level(3)
        await callback.answer("Уровень детализации изменен на 3")

