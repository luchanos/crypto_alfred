from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton("Написать админу ✍️")
b2 = KeyboardButton("Справка ❓")
b3 = KeyboardButton("Реферальная ссылка 🤝")
b4 = KeyboardButton("Мой кошелек 💰")
b5 = KeyboardButton("Поделиться рейтингом 💸")

main_keyboard.row(b4, b5).row(b1, b2).add(b3)
