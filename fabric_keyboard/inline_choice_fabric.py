from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from fabric_keyboard.main_fabirc import MainFabric


class InlineChoiceSettings(CallbackData, prefix="inline_choice_settings"):
    setting_action: str


class InlineChoiceMode(CallbackData, prefix="inline_choice_mode"):
    mode: str


class InlineChoiceFabric(MainFabric):

    async def choice_fabric(self) -> InlineKeyboardMarkup:
        await self.create_builder_inline()

        settings_button = InlineKeyboardButton(
            text="Выберите режим",
            callback_data=InlineChoiceSettings(
                setting_action="settings",
            ).pack()
        )

        self.builder_inline.add(settings_button)

        return self.builder_inline.as_markup()

    async def choice_mode(self, last_mode: str) -> InlineKeyboardMarkup:
        await self.create_builder_inline()
        print(last_mode)
        choice_mode_button = InlineKeyboardButton(
            text=f"Краткое описание{'✅' if last_mode == 'short_description' else '❌'}",
            callback_data=InlineChoiceMode(
                mode="short_description",
            ).pack()
        )

        cancel_button = InlineKeyboardButton(
            text="Назад",
            callback_data=InlineChoiceMode(
                mode="cancel",
            ).pack()
        )

        self.builder_inline.add(choice_mode_button)
        self.builder_inline.row(cancel_button)

        return self.builder_inline.as_markup()

