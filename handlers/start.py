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
        await message.answer("Hello again 👋 What do you want to do?", reply_markup=main_keyboard)
    else:
        await FormAcceptRules.accept_rules.set()
        await message.answer(
            text="Greetings! Check out the chat rules. Do you agree with them?\n"
            "https://teletype.in/@coiners/Um4d1JbBAgD.",
            reply_markup=accept_rules_keyboard,
        )


async def accept_rules_state(message: types.Message, state: FSMContext):
    if message.text == "I accept":
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
            f"Excellent!\nHere is the link to join the group: {await create_invite_link(message)}\n\n"
            f"You can always get acquainted with our referral system, write to the admin, or request "
            f"a referral link to invite a friend and earn yourself a rating 😎",
            reply_markup=main_keyboard,
        )
        await state.reset_state()
    elif message.text == "Do not Accept":
        await message.answer(
            "Unfortunately! 😓\nWithout accepting the terms, we will not be able to accept you into the community!",
            reply_markup=accept_rules_keyboard,
        )


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(accept_rules_state, content_types=["text"], state=FormAcceptRules.accept_rules)
    dp.register_message_handler(start, Text(equals=f"Join the group 🤑"))
