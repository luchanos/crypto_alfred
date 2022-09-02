import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked

from clients.users_api_client import get_user, recreate_user
from keyboards import accept_rules_keyboard, main_keyboard, set_lang_keyboard
from settings import CHAT_ID_GROUP
from setup_bot import _


class FormAcceptRulesReferral(StatesGroup):
    accept_rules_referral = State()


async def start_set_lang(message: types.ChatJoinRequest):
    retry_cnt = 10
    while retry_cnt > 0:
        try:
            await message.bot.send_message(
                chat_id=message.from_user.id,
                text="Please, choose language",
                reply_markup=set_lang_keyboard(),
            )
            break
        except BotBlocked:
            retry_cnt -= 1
            await asyncio.sleep(5)


async def start_for_referrals(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        await FormAcceptRulesReferral.accept_rules_referral.set()
        await message.answer(
            text=_(
                "Hello! Before joining the group, please read the chat rules. Do you "
                "agree with them?\n\nhttps://teletype.in/@coiners/Um4d1JbBAgD."
            ),
            reply_markup=accept_rules_keyboard(),
        )


async def accept_rules_referral(message: types.Message, state: FSMContext):
    if message.text in ("I accept", "Принимаю", "ვღებულობ"):
        await recreate_user(message.from_user.id)
        await message.answer(text=_("Excellent! Welcome to chat!"), reply_markup=main_keyboard())
        await message.bot.approve_chat_join_request(user_id=message.from_user.id, chat_id=CHAT_ID_GROUP)
        await state.finish()
    elif message.text in ("Do not Accept", "Не принимаю", "არ ვღებულობ"):
        await message.answer(
            text=_(
                "It's a pity! 😓\nWithout accepting the terms, we will "
                "not be able to accept you to join the community!"
            ),
            reply_markup=accept_rules_keyboard(),
        )


def register_handlers_start_for_referrals(dp: Dispatcher):
    dp.register_chat_join_request_handler(start_set_lang)
    dp.register_message_handler(start_for_referrals, Text(equals=["Русский 🇷🇺", "English 🇬🇧", "ქართული 🇬🇪"]))
    dp.register_message_handler(
        accept_rules_referral, content_types=["text"], state=FormAcceptRulesReferral.accept_rules_referral
    )
