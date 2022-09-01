from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def stop_send_rating_keyboard():
    b1 = KeyboardButton(_("Cancel ❌"))

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(b1)
    return keyboard
