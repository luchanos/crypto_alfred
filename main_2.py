import json
import telebot
from envparse import Env
from telebot.types import Message
from telebot import types

env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.str("ADMIN_CHAT_ID")

bot = telebot.TeleBot(TOKEN)


def register_new_user(user_id: int, chat_id: int):
    with open("users.json", "r") as f_o:
        users = json.load(f_o)
        if str(user_id) not in users:
            users[user_id] = {
                "rating": 0,
                "status": "Mr. Andersen",
                "accepted_rules": False,
                "chat_id": chat_id
            }
    with open("users.json", "w") as f_o:
        json.dump(users, f_o, indent=4, ensure_ascii=False)


def accept_rules_by_user(bot, message, markup):
    bot.reply_to(message, "Отлично!", reply_markup=markup)
    user_id = str(message.from_user.id)
    with open("users.json", "r") as f_o:
        users = json.load(f_o)
    user_info = users[user_id]
    user_info["accepted_rules"] = True
    with open("users.json", "w") as f_o:
        json.dump(users, f_o, indent=4, ensure_ascii=False)


def generate_greet_message():
    return """Приветствую! Ознакомьтесь с правилами чата: правила чата.
Согласны ли вы с ними?"""


def menu_chooser(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Написать админу')
    itembtn2 = types.KeyboardButton('Указать уровень знаний')
    itembtn3 = types.KeyboardButton('Ознакомиться с рейтинговой системой')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Добро пожаловать в меню', reply_markup=markup)


def proceed_accept_rules_answer(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    answer = message.text.strip()
    if answer == "Принимаю":
        accept_rules_by_user(bot, message, markup)
        menu_chooser(message)
    else:
        bot.reply_to(message, "Жаль, без этого мы не сможем принять тебя в сообщество!", reply_markup=markup)


@bot.message_handler(commands=["start"])
def start(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    register_new_user(user_id, chat_id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Принимаю')
    itembtn2 = types.KeyboardButton('Не принимаю')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, generate_greet_message(), reply_markup=markup)
    bot.register_next_step_handler(message, proceed_accept_rules_answer)


while True:
    try:
        bot.polling()
    except Exception as err:
        print(err)
