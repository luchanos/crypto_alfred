from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from clients.tg_client import create_invite_link
from clients.users_api_client import get_user, is_deleted_user, recreate_user, register_new_user
from keyboards import accept_rules_keyboard, main_keyboard


class FormAcceptRules(StatesGroup):
    accept_rules = State()


async def start(message: types.Message) -> None:
    user = await get_user(message.from_user.id)
    if user and user.get("accept_rules"):
        await message.answer("И снова Здравствуйте 👋 Что хочешь сделать ?", reply_markup=main_keyboard)
    else:
        await FormAcceptRules.accept_rules.set()
        await message.answer(
            text="Приветствую! Ознакомьтесь с правилами чата. Согласны ли вы с ними?\n"
            "https://teletype.in/@coiners/Um4d1JbBAgD.",
            reply_markup=accept_rules_keyboard,
        )


async def accept_rules_state(message: types.Message, state: FSMContext):
    if message.text == "Принимаю":
        user_id = message.from_user.id
        chat_id = message.chat.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        if await is_deleted_user(user_id):
            await recreate_user(user_id)
        else:
            await register_new_user(user_id, chat_id, username, first_name, last_name)
        await message.answer(
            f"Отлично!\nВот ссылка на вступление в группу {await create_invite_link(message)}\n\n"
            f"Ты всегда можешь ознакомиться с нашей реферальной системой, написать админу или запросить "
            f"реферальную ссылку, чтобы пригласить друга и заработать себе рейтинг 😎",
            reply_markup=main_keyboard,
        )
        await state.reset_state()
    elif message.text == "Не принимаю":
        await message.answer(
            "Очень жаль 😓\nБез принятия условий мы не сможем принять тебя в сообщество !",
            reply_markup=accept_rules_keyboard,
        )


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(accept_rules_state, content_types=["text"], state=FormAcceptRules.accept_rules)
    dp.register_message_handler(start, Text(equals=f"Присоединиться к группе 🤑"))
