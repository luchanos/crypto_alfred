from typing import Union

import telebot
from envparse import Env
from mongoengine import DoesNotExist
from telebot.types import Message, ChatMemberUpdated
from telebot import types, util

from mongo_models import User
from raw_telegram_client import TelegramClientRaw
from mongoengine import connect

env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.str("ADMIN_CHAT_ID")
BASE_TG_URL = env.str("TELEGRAM_BASE_URL", default="https://api.telegram.org")
MAIN_CHAT_ID = env.str("MAIN_CHAT_ID")
MONGO_DB_NAME = env.str("MONGO_DB_NAME", default="crypto_alfred_db")


class CustomBot(telebot.TeleBot):
    def __init__(self, tg_client: TelegramClientRaw, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = tg_client


with open("bad_words.txt") as f_o:
    BAD_WORDS = f_o.readlines()

tg_client = TelegramClientRaw(token=TOKEN, base_url=BASE_TG_URL)
bot = CustomBot(token=TOKEN, tg_client=tg_client)
connect(MONGO_DB_NAME)


def get_user(user_id: int) -> Union[User, None]:
    try:
        user = User.objects.get(user_id=user_id)
    except DoesNotExist as err:
        print(user_id, err)
        return
    return user


def register_new_user(user_id: int, chat_id: int) -> User:
    user = get_user(user_id)
    if user is None:
        user = User(user_id=user_id, chat_id=str(chat_id)).save()
    return user


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
    User.objects(user_id=message.from_user.id).update_one(set__level=level)
    bot.reply_to(message, "Отлично! Для углубления своих знаний рекомендуем ознакомиться со"
                          "следующими статьями: ############", reply_markup=markup)


def proceed_accept_rules_answer(message: Message):
    markup = types.ReplyKeyboardRemove(selective=False)
    answer = message.text.strip()
    if answer == "Принимаю":
        User.objects(user_id=message.from_user.id).update_one(set__accepted_rules=True)
        bot.reply_to(message, "Отлично!", reply_markup=markup)
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
    bot.reply_to(message, """Приветствую! Ознакомьтесь с правилами чата: https://teletype.in/@coiners/Um4d1JbBAgD.
Согласны ли вы с ними?""", reply_markup=markup)
    bot.register_next_step_handler(message, proceed_accept_rules_answer)


def get_referal_link(user_id):
    user = get_user(user_id)
    referal_link = user.referal_link
    if referal_link is None:
        generated_link_data = bot.tg_client.generate_invite_link(chat_id=MAIN_CHAT_ID)
        referal_link = generated_link_data.get("result").get("invite_link")
        user.referal_link = referal_link
        user.save()
    return referal_link


@bot.message_handler(commands=["give_me_referal_link"])
def give_me_referal_link(message):
    referal_link = get_referal_link(message.from_user.id)
    bot.reply_to(message, text=f"Вот твоя реферальная ссылка: {referal_link}")


@bot.chat_member_handler()
def handle_invites_via_link(message):
    if isinstance(message, ChatMemberUpdated):
        # todo тут сделать так, чтобы писать в логи и оповещать пользователя что ему начислили рейтинг
        User.objects(referal_link=message.invite_link.invite_link).update_one(inc__rating=1)


@bot.message_handler(content_types=["text"])
def bad_language_moderator(message):
    for bad_word in BAD_WORDS:
        if bad_word.strip() in message.text:
            bot.reply_to(message, text="Не ругайся!")
            break


while True:
    try:
        bot.polling(allowed_updates=util.update_types)
    except Exception as err:
        print(err)
