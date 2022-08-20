from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


confirmation_send_rating_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton("Да")
b2 = KeyboardButton("Нет")

confirmation_send_rating_keyboard.row(b1, b2)