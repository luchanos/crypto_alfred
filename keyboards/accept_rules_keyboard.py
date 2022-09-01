from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def accept_rules_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    b1 = KeyboardButton(_("I accept"))
    b2 = KeyboardButton(_("Do not Accept"))

    keyboard.row(b1, b2)
    return keyboard
