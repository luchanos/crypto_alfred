from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


confirmation_send_rating_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton("Yes")
b2 = KeyboardButton("No")

confirmation_send_rating_keyboard.row(b1, b2)
