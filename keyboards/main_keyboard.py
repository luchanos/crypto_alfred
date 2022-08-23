from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton("Write to admin ✍️")
b2 = KeyboardButton("Reference ❓")
b3 = KeyboardButton("Referral link 🤝")
b4 = KeyboardButton("My wallet 💰")
b5 = KeyboardButton("Share rating 💸")
b6 = KeyboardButton("Exchange rates 💲")

main_keyboard.row(b4, b5).row(b1, b2).row(b3, b6)
