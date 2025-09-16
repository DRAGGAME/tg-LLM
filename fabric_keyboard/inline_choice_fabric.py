from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from fabric_keyboard.main_fabirc import MainFabric


class InlineChoiceSettings(CallbackData, prefix="inline_choice_settings"):
    setting_action: str


class InlineChoiceMode(CallbackData, prefix="inline_choice_mode"):
    mode: str


class InlineChoiceTextSettings(CallbackData, prefix="inline_choice_text_settings"):
    mode_for_text: str


class InlineChoiceLevel(CallbackData, prefix="inline_choice_level"):
    level: int


class QuestionLevelChoice(CallbackData, prefix="questions_choice"):
    question_level: int


class InlineChoiceFabric(MainFabric):

    def __init__(self):

        self.cancel_button = InlineKeyboardButton(
            text="Назад",
            callback_data=InlineChoiceMode(
                mode="cancel",
            ).pack()
        )

        super().__init__()


    async def choice_fabric(self) -> InlineKeyboardMarkup:
        await self.create_builder_inline()

        settings_button = InlineKeyboardButton(
            text="Выберите режим",
            callback_data=InlineChoiceSettings(
                setting_action="settings",
            ).pack()
        )

        big_text_button = InlineKeyboardButton(
            text="Настройки текста",
            callback_data=InlineChoiceSettings(
                setting_action="settings_text",
            ).pack(),
        )

        run_button = InlineKeyboardButton(
            text="Запустить",
            callback_data=InlineChoiceSettings(
                setting_action="run",
            ).pack()
        )

        self.builder_inline.add(settings_button)
        self.builder_inline.row(big_text_button)
        self.builder_inline.row(run_button)

        return self.builder_inline.as_markup()

    async def choice_mode(self, last_mode: str) -> InlineKeyboardMarkup:
        await self.create_builder_inline()
        print(last_mode)
        choice_mode_button = InlineKeyboardButton(
            text=f"Краткое описание{'✅' if last_mode[0][0] == 'short_description' else '❌'}",
            callback_data=InlineChoiceMode(
                mode="short_description",
            ).pack()
        )

        self.builder_inline.add(choice_mode_button)
        self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()

    async def choice_settings_text(self, last_mode: str) -> InlineKeyboardMarkup:
        await self.create_builder_inline()

        if last_mode == "short_description":

            size_button = InlineKeyboardButton(
                text="Размер текста",
                callback_data=InlineChoiceTextSettings(
                    mode_for_text="Вдумчивость",
                ).pack()
            )

            details_button = InlineKeyboardButton(
                text="Углублённость вопросов",
                callback_data=InlineChoiceTextSettings(
                    mode_for_text="Questions",
                ).pack()
            )

            self.builder_inline.row(size_button, details_button)
            self.builder_inline.row(self.cancel_button)

        else:
            self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()

    async def change_question_data(self, number_activity: int=1) -> InlineKeyboardMarkup:
        await self.create_builder_inline()

        level_button_one = InlineKeyboardButton(
            text=f"1{'✅' if number_activity == 1 else '❌'}",
            callback_data=InlineChoiceLevel(
                level=1,
            ).pack()
        )

        level_button_two = InlineKeyboardButton(
            text=f"2{'✅' if number_activity == 2 else '❌'}",
            callback_data=InlineChoiceLevel(
                level=2,
            ).pack()
        )

        level_button_three = InlineKeyboardButton(
            text=f"3{'✅' if number_activity == 3 else '❌'}",
            callback_data=InlineChoiceLevel(
                level=3,
            ).pack()
        )

        self.builder_inline.row(level_button_one, level_button_two, level_button_three)
        self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()

    async def choice_question_level(self, level_activity: int=1) -> InlineKeyboardMarkup:

        await self.create_builder_inline()

        level_button_one = InlineKeyboardButton(
            text=f"1{'✅' if level_activity == 1 else '❌'}",
            callback_data=QuestionLevelChoice(
                question_level=1,
            ).pack()
        )

        level_button_two = InlineKeyboardButton(
            text=f"2{'✅' if level_activity == 2 else '❌'}",
            callback_data=QuestionLevelChoice(
                question_level=2,
            ).pack()
        )

        level_button_three = InlineKeyboardButton(
            text=f"3{'✅' if level_activity == 3 else '❌'}",
            callback_data=QuestionLevelChoice(
                question_level=3,
            ).pack()
        )

        self.builder_inline.row(level_button_one, level_button_two, level_button_three)
        self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()
