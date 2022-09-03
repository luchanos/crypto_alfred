from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def is_delete_user(locale):
    b1 = KeyboardButton(_("Join the group 🤑", locale=locale))

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(b1)
    return keyboard
