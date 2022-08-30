import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked

from clients.users_api_client import get_user, is_deleted_user, recreate_user, register_new_user
from keyboards import accept_rules_keyboard, main_keyboard
from settings import CHAT_ID_GROUP


async def start_for_referrals(message: types.ChatJoinRequest):
    retry_cnt = 10
    while retry_cnt > 0:
        try:
            await message.bot.send_message(
                chat_id=message.from_user.id,
                text="Hello! Before joining the group, please read the chat rules. Do you "
                "agree with them?\n\nhttps://teletype.in/@coiners/Um4d1JbBAgD.",
                reply_markup=accept_rules_keyboard,
            )
            break
        except BotBlocked:
            retry_cnt -= 1
            await asyncio.sleep(5)


async def accept_rules_referral(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
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
            await message.answer(text="Excellent! Welcome to chat!", reply_markup=main_keyboard)
            await message.bot.approve_chat_join_request(user_id=message.from_user.id, chat_id=CHAT_ID_GROUP)
        elif message.text == "Do not accept":
            await message.answer(
                text="Unfortunately! 😓\nWithout accepting the terms, we "
                "will not be able to accept you into the community!",
                reply_markup=accept_rules_keyboard,
            )


def register_handlers_start_for_referrals(dp: Dispatcher):
    dp.register_chat_join_request_handler(start_for_referrals)
    dp.register_message_handler(accept_rules_referral, Text(equals=("I accept", "Do not accept", "/start")))
