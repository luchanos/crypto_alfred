from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def confirmation_send_rating_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    b1 = KeyboardButton(_("Yes"))
    b2 = KeyboardButton(_("No"))

    keyboard.row(b1, b2)
    return keyboard
