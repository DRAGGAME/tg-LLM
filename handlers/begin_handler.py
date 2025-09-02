from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceFabric, InlineChoiceSettings, InlineChoiceMode

begin_router = Router(name="begin_router")
keyboard_choice = InlineChoiceFabric()
sqlite = UserQueries()

@begin_router.message(CommandStart())
async def start_handler(message: Message):
    kb = await keyboard_choice.choice_fabric()
    await sqlite.connect()

    user_id = message.from_user.id
    username = message.from_user.username
    data = await sqlite.get_user_model(str(user_id))
    if data:
        await sqlite.insert_user(username, str(user_id))

    await message.answer("Приветствую вас, вы зашли в меню настроек. Что вы хотите изменить?", reply_markup=kb)


@begin_router.callback_query(InlineChoiceMode.filter(F.mode=="cancel"))
async def cancel_handler(callback: CallbackQuery):
    kb = await keyboard_choice.choice_fabric()

    await callback.message.edit_text("Вы зашли в меню настроек. Что вы хотите изменить?", reply_markup=kb)
    await callback.answer()

@begin_router.callback_query(InlineChoiceSettings.filter(F.setting_action=="settings"))
async def settings_handler(callback: CallbackQuery):
    await sqlite.connect()
    model = await sqlite.get_user_model(str(callback.from_user.id))
    kb = await keyboard_choice.choice_mode(model)

    await callback.message.edit_text("Выберите режим работы", reply_markup=kb)
    await callback.answer()