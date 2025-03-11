# keyboard/user_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_user_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Показать профиль")]
        ],
        resize_keyboard=True
    )
