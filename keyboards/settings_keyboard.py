from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import User


class Settings(CallbackData, prefix="prop"):
    action: str


def get(user: User) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(
        text=f'{["Вкл", "Выкл"][user.autoend]} автозавершение',
        callback_data=Settings(action='autoend').pack()
    ))

    if user.autoend:
        kb.add(InlineKeyboardButton(
            text=f'Время автозавершения',
            callback_data=Settings(action='autoendtime').pack()
        ))

    kb.row(InlineKeyboardButton(
        text='Изменить имя',
        callback_data=Settings(action='name').pack()
    ))

    return kb.as_markup()


