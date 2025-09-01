from sys import prefix
from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

class InlineAddAdmin(CallbackData, prefix="AddAdmins"):
    action: str


class KeyboardFactory:

    def __init__(self):
        self.builder_reply = None

        self.builder_inline = None

    async def create_builder_reply(self) -> None:
        self.builder_reply = ReplyKeyboardBuilder()

    async def create_builder_inline(self) -> None:
        self.builder_inline = InlineKeyboardBuilder()

    async def builder_inline_add_admins(self):
        await self.create_builder_inline()

        add_button = InlineKeyboardButton(
            text="Принять",
            callback_data=InlineAddAdmin(
                action="accept",
            ).pack()
        )

        cancel_button = InlineKeyboardButton(
            text="Отклонить",
            callback_data=InlineAddAdmin(
                action="reject",
            ).pack()
        )

        self.builder_inline.add(add_button)
        self.builder_inline.row(cancel_button)

        return self.builder_inline.as_markup()

