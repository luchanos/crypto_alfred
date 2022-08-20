from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


accept_rules_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton(f"Принимаю")
b2 = KeyboardButton(f"Не принимаю")

accept_rules_keyboard.row(b1, b2)
