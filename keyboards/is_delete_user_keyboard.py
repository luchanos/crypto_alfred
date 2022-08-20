from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton("Присоединиться к группе 🤑")

is_delete_user = ReplyKeyboardMarkup(resize_keyboard=True)
is_delete_user.row(b1)
