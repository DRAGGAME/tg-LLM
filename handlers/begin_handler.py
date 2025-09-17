from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import bot
from database.user_queries import UserQueries
from fabric_keyboard.inline_choice_fabric import InlineChoiceFabric, InlineChoiceSettings, InlineChoiceMode

begin_router = Router(name="begin_router")
keyboard_choice = InlineChoiceFabric()
sqlite = UserQueries()


@begin_router.message(CommandStart())
async def start_handler(message: Message):
    await sqlite.connect()

    user_id = message.from_user.id
    username = message.from_user.username

    data = await sqlite.get_user_model(str(user_id))
    if not data:
        await sqlite.insert_user(username, str(user_id))

    # await bot.unpin_all_chat_messages(chat_id=message.chat.id)
    await sqlite.close()
    await message.answer(f"Приветствую вас, пришлите файл и настройте")

    # await bot_message.pin()


@begin_router.callback_query(InlineChoiceMode.filter(F.mode == "cancel"))
async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    kb = await keyboard_choice.choice_fabric()

    level = await state.get_value("level")
    level_question = await state.get_value("level_question")

    print(level, level_question)

    if level:
        level = 1
        await state.update_data(level=level)

    if level_question:
        level_question = 1
        await state.update_data(level_question=level_question)

    message_text = ("Какие параметры вы будете использовать?\n\n"
                  f"Текущий уровень углублённости вопросов: {level_question}\n"
                  f"Текущий уровень детализации: {level}")

    await callback.message.edit_text(f"{message_text}", reply_markup=kb)
    await callback.answer()
