from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from fabric_keyboard.inline_choice_fabric import InlineChoiceSize

settings_router = Router(name="settings_router")

@settings_router.callback_query(InlineChoiceSize.filter(F.size_text.in_([1, 2, 3])))
async def change_size_one(callback: CallbackQuery, callback_data: CallbackData):
    if callback_data.size_text == 1:
        await callback.answer("Размер текста изменен на 1")
    elif callback_data.size_text == 2:
        await callback.answer("Размер текста изменен на 2")
    elif callback_data.size_text == 3:
        await callback.answer("Размер текста изменен на 3")

