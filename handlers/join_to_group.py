from aiogram import Dispatcher, types

from clients.users_api_client import (
    delete_user,
    get_user,
    get_user_by_referral_link,
    update_common_rating_referral,
)
from keyboards import is_delete_user
from settings import CHAT_ID_GROUP, REFERRAL_COUNT_FOR_COMMON_RATING


async def new_chat_member(message: types.ChatMemberUpdated):
    status = message.new_chat_member.status
    invite_link = message.invite_link.invite_link if message.invite_link else ""
    user = await get_user(message.new_chat_member.user.id)

    # если пользователь присоединился к чату
    if status == "member":
        if user.get("join_to_group_count") == 1:
            res = await update_common_rating_referral(invite_link)
            if res.get("user_id"):
                await message.bot.send_message(
                    chat_id=res.get("user_id"),
                    text=f"Вам начислено {REFERRAL_COUNT_FOR_COMMON_RATING} очков рейтинга за приглашенного друга 💪",
                )
        else:
            user_with_referral_link = await get_user_by_referral_link(invite_link)
            if user_with_referral_link.get("user_id"):
                await message.bot.send_message(
                    chat_id=user_with_referral_link.get("user_id"),
                    text=f"К сожалению, мы не можем начислить вам рейтинг, так как ваш "
                    f"приглашенный друг уже состоял в нашей группе 😢",
                )
        await message.bot.promote_chat_member(
            CHAT_ID_GROUP, message.new_chat_member.user.id, can_pin_messages=True
        )
        await message.bot.set_chat_administrator_custom_title(
            CHAT_ID_GROUP, message.new_chat_member.user.id, user.get("rating_status")
        )

    # если пользователь покинул чат
    elif status == "left":
        if user.get("referral_link"):
            await message.bot.revoke_chat_invite_link(CHAT_ID_GROUP, user.get("referral_link"))
        await delete_user(message.new_chat_member.user.id)
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text="Очень жаль, что вы покинули группу 😢\nВ любое время вы можете попросить снова вступить в группу. "
            "Ваш рейтинг при этом сохраниться !",
            reply_markup=is_delete_user,
        )


def register_handlers_join_to_group(dp: Dispatcher):
    dp.register_chat_member_handler(new_chat_member)
