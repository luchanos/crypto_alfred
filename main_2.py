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


@bot.message_handler(commands=["menu"])
def menu_chooser_main(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Написать админу')
    itembtn2 = types.KeyboardButton('Указать уровень знаний')
    itembtn3 = types.KeyboardButton('Ознакомиться с рейтинговой системой')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Добро пожаловать в меню', reply_markup=markup)
    bot.register_next_step_handler(message, menu_chooser_submain)


def menu_chooser_submain(message):
    answer = message.text.strip()
    if answer == 'Указать уровень знаний':
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Новичок')
        itembtn2 = types.KeyboardButton('Середнячок')
        itembtn3 = types.KeyboardButton('Профи')
        itembtn4 = types.KeyboardButton('Бог')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.reply_to(message, 'Укажите свой уровень знаний', reply_markup=markup)
        bot.register_next_step_handler(message, write_knowledge_level)
    elif answer == 'Ознакомиться с рейтинговой системой':
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.reply_to(message, 'Вот наша рейтинговая система: ############', reply_markup=markup)
    elif answer == 'Написать админу':
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.register_next_step_handler(message, write_to_admin)
        bot.reply_to(message, 'Что хотите написать?', reply_markup=markup)


def write_to_admin(message):
    msg_to_admin = message.text.strip()
    bot.reply_to(message, "Ваше обращение зарегистрировано!")


def write_knowledge_level(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    level = message.text.strip()
    user_id = str(message.from_user.id)
    bot.reply_to(message, "Отлично! Для углубления своих знаний рекомендуем ознакомиться со"
                          "следующими статьями: ############", reply_markup=markup)
    with open("users.json", "r") as f_o:
        users = json.load(f_o)
    user_info = users[user_id]
    user_info["level"] = level
    with open("users.json", "w") as f_o:
        json.dump(users, f_o, indent=4, ensure_ascii=False)


def proceed_accept_rules_answer(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    answer = message.text.strip()
    if answer == "Принимаю":
        accept_rules_by_user(bot, message, markup)
        menu_chooser_main(message)
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
    bot.reply_to(message, """Приветствую! Ознакомьтесь с правилами чата: правила чата.
Согласны ли вы с ними?""", reply_markup=markup)
    bot.register_next_step_handler(message, proceed_accept_rules_answer)


while True:
    try:
        bot.polling()
    except Exception as err:
        print(err)
