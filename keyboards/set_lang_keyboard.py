from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def set_lang_keyboard():
    lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    b1 = KeyboardButton("Русский 🇷🇺")
    b2 = KeyboardButton("English 🇬🇧")
    b3 = KeyboardButton("ქართული 🇬🇪")

    lang_keyboard.row(b1, b2, b3)
    return lang_keyboard
