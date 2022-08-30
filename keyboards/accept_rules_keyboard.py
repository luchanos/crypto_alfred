from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


accept_rules_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton(f"I accept")
b2 = KeyboardButton(f"Do not Accept")

accept_rules_keyboard.row(b1, b2)
