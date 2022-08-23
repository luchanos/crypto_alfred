from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton("Cancel 🔙")

write_to_admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
write_to_admin_keyboard.row(b1)
