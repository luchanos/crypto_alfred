from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from setup_bot import _


def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    b1 = KeyboardButton(_("Write to admin ✍️"))
    b2 = KeyboardButton(_("Reference ❓"))
    b3 = KeyboardButton(_("Referral link 🤝"))
    b4 = KeyboardButton(_("My wallet 💰"))
    b5 = KeyboardButton(_("Share rating 💸"))
    b6 = KeyboardButton(_("Exchange rates 💲"))

    keyboard.row(b4, b5).row(b1, b2).row(b3, b6)
    return keyboard
