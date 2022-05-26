import json
import telebot
from envparse import Env
from telebot.types import Message
from telebot import types

from raw_telegram_client import TelegramClientRaw

env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.str("ADMIN_CHAT_ID")
BASE_TG_URL = "https://api.telegram.org"
MAIN_CHAT_ID = env.str("MAIN_CHAT_ID")


class CustomBot(telebot.TeleBot):
    def __init__(self, tg_client: TelegramClientRaw, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = tg_client


with open("bad_words.txt") as f_o:
    BAD_WORDS = f_o.readlines()

tg_client = TelegramClientRaw(token=TOKEN, base_url=BASE_TG_URL)
bot = CustomBot(token=TOKEN, tg_client=tg_client)


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
    bot.reply_to(message, "Ваше обращение зарегистрировано!")
    bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Пользователь @{message.from_user.username} оставил обращение:"
                                                 f" «{message.text.strip()}»")


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


def get_referal_link_from_db(user_id):
    with open("users.json", "r") as f_o:
        links = json.load(f_o)
        user_link = links.get(str(user_id)).get("referal_link")
        if user_link is not None:
            return user_link
    generated_link_data = bot.tg_client.generate_invite_link(chat_id=MAIN_CHAT_ID)
    user_link = generated_link_data.get("result").get("invite_link")
    if user_link is not None:
        with open("invited_links.json", "r") as f_o:
            links = json.load(f_o)
            links[user_link] = str(user_id)
        with open("invited_links.json", "w") as f_o:
            json.dump(links, f_o, indent=4, ensure_ascii=False)
        with open("users.json", "r") as f_o:
            users = json.load(f_o)
        with open("users.json", "w") as f_o:
            users[str(user_id)]["referal_link"] = user_link
            json.dump(users, f_o, indent=4, ensure_ascii=False)
        return user_link
    raise Exception("Smth went wrong due to generation referal link. Generated data: ", generated_link_data)


@bot.message_handler(commands=["give_me_referal_link"])
def give_me_referal_link(message):
    referal_link = get_referal_link_from_db(message.from_user.id)
    bot.reply_to(message, text=f"Вот твоя реферальная ссылка: {referal_link}")


@bot.message_handler(content_types=["text"])
def bad_language_moderator(message):
    for bad_word in BAD_WORDS:
        if bad_word.strip() in message.text:
            bot.reply_to(message, text="Не ругайся!")
            break


while True:
    try:
        bot.polling()
    except Exception as err:
        print(err)
