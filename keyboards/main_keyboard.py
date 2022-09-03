from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def main_keyboard(locale: str = None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    b1 = KeyboardButton(_("My wallet 💰", locale=locale))
    b2 = KeyboardButton(_("Send 💸", locale=locale))
    b3 = KeyboardButton(_("Referral link 🤝", locale=locale))
    b4 = KeyboardButton(_("Language 🌐", locale=locale))
    b5 = KeyboardButton(_("Write to administration ✍️", locale=locale))

    keyboard.row(b1, b2).row(b3, b4).row(b5)
    return keyboard
