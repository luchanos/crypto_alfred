from datetime import datetime, timedelta

from aiogram.types import Message

from clients.users_api_client import get_user, update_referral_link
from settings import CHAT_ID_GROUP
from setup_bot import bot


def check_permissions(func):
    async def inner(message: Message, *args, **kwargs):
        user = await get_user(message.from_user.id)
        if user.get("accept_rules"):
            return await func(message, *args, **kwargs)
        await message.answer("Вы не приняли правила! Вы не можете этого делать!")

    return inner


async def create_invite_link(message: Message):
    expire_date = datetime.now() + timedelta(days=1)
    link = await message.bot.create_chat_invite_link(CHAT_ID_GROUP, expire_date, member_limit=1)
    return link.invite_link


async def get_invite_link(chat_id: int):
    await bot.tg_client.generate_invite_link(chat_id)


async def get_referral_link(message: Message):
    user = await get_user(message.from_user.id)
    if not user.get("referral_link"):
        chat_invite_link = await message.bot.create_chat_invite_link(
            chat_id=CHAT_ID_GROUP, creates_join_request=True
        )
        link = chat_invite_link.invite_link
        await update_referral_link(message.from_user.id, link)
        return link
    return user.get("referral_link")
