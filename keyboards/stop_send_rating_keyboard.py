from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton("Cancel ❌")

stop_send_rating_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
stop_send_rating_keyboard.row(b1)
