from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import bot
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
    if not data:
        await sqlite.insert_user(username, str(user_id))

    # await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    await sqlite.close()
    await message.answer(f"Приветствую вас, пришлите файл и настройте", reply_markup=kb)

    # await bot_message.pin()


@begin_router.callback_query(InlineChoiceMode.filter(F.mode == "cancel"))
async def cancel_handler(callback: CallbackQuery):
    kb = await keyboard_choice.choice_fabric()

    await callback.message.edit_text("Вы зашли в меню настроек. Что вы хотите изменить?", reply_markup=kb)
    await callback.answer()


