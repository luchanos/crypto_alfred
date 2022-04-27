from telebot import TeleBot, types
from envparse import Env

from messages_templates import GREETINGS_MESSAGE, LEVEL_QUESTION, TEACHING_PROPOSING

env = Env()

TOKEN = env.str("TOKEN", default="5268184663:AAFq5p4mBwKHxK6wjFlRHs2d_v7mYAWfeqc")

bot = TeleBot(TOKEN)


def write_msg_to_admin(message):
    bot.reply_to(message, "Спасибо! Твоё сообщение зарегистрировано под номером 666. Жди ответа!")


def message_to_admin(message):
    chat_id = message.chat.id
    if message.text == 'Да':
        bot.register_next_step_handler(message, write_msg_to_admin)
    else:
        bot.send_message(chat_id, "Хорошо! Если что - пиши ;) ")


def level_question(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id, f"Спасибо за ответ! Вы выбрали уровень: {message.text}", reply_markup=markup)
    bot.send_message(chat_id, TEACHING_PROPOSING)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    bot.send_message(chat_id, "Желаешь оставить сообщение администратору?")
    markup.add(itembtn1, itembtn2)
    bot.register_next_step_handler(message, message_to_admin)


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, text=GREETINGS_MESSAGE)
    bot.send_message(message.chat.id, text=LEVEL_QUESTION)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Нет знаний')
    itembtn2 = types.KeyboardButton('Начинающий')
    itembtn3 = types.KeyboardButton('Разбираюсь')
    itembtn4 = types.KeyboardButton('Спец')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)
    bot.register_next_step_handler(message, level_question)


bot.polling()
