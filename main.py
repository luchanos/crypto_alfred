from telebot import TeleBot, types
from envparse import Env
import logging

from messages_templates import GREETINGS_MESSAGE, LEVEL_QUESTION, TEACHING_PROPOSING

env = Env()
logger = logging.getLogger(__name__)

TOKEN = env.str("TOKEN")

bot = TeleBot(TOKEN)


def write_msg_to_admin(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message,
                 "Спасибо! Твоё сообщение зарегистрировано под номером 666. Жди ответа!",
                 reply_markup=markup)


def message_to_admin(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    if message.text == 'Да':
        bot.register_next_step_handler(message, write_msg_to_admin)
        bot.send_message(chat_id, "Очень внимательно тебя слушаю")
    else:
        bot.send_message(chat_id, "Хорошо! Если что - пиши ;) ", reply_markup=markup)


def level_question(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, f"Спасибо за ответ! Вы выбрали уровень: {message.text}", reply_markup=markup)
    bot.send_message(chat_id, TEACHING_PROPOSING)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    bot.send_message(chat_id, "Желаешь оставить сообщение администратору?", reply_markup=markup)
    bot.register_next_step_handler(message, message_to_admin)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, text=GREETINGS_MESSAGE)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Нет знаний')
    itembtn2 = types.KeyboardButton('Начинающий')
    itembtn3 = types.KeyboardButton('Разбираюсь')
    itembtn4 = types.KeyboardButton('Спец')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(chat_id, LEVEL_QUESTION, reply_markup=markup)
    bot.register_next_step_handler(message, level_question)


try:
    bot.polling()
except Exception as err:
    logger.error(err)
