from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from clients.tg_client import create_invite_link
from clients.users_api_client import get_deleted_user, get_user, recreate_user
from keyboards import accept_rules_keyboard, main_keyboard, set_lang_keyboard
from setup_bot import _


class FormAcceptRules(StatesGroup):
    set_lang = State()
    accept_rules = State()


async def start(message: types.Message):
    user = await get_user(message.from_user.id)

    if user and user.get("accept_rules"):
        await message.answer(_("Hello again 👋 What do you want to do?"), reply_markup=main_keyboard())
    else:
        deleted_user = await get_deleted_user(message.from_user.id)

        # if joining for the first time
        if deleted_user.get("join_to_group_count") == 0:
            await FormAcceptRules.set_lang.set()
            await message.answer_sticker("CAACAgIAAxkBAAEFwHRjFFPnOMR1xAKqg3cX6LEMSjhshgACVAADQbVWDGq3-McIjQH6KQQ")
            await message.answer("Please, choose language", reply_markup=set_lang_keyboard())
        else:
            await FormAcceptRules.accept_rules.set()
            await message.answer(
                text=_(
                    "Greetings! Check out the chat rules. Do you agree with them?\n"
                    "https://teletype.in/@coiners/Um4d1JbBAgD."
                ),
                reply_markup=accept_rules_keyboard(),
            )


async def set_lang(message: types.Message, state: FSMContext):
    await FormAcceptRules.next()
    await message.answer(
        text=_(
            "Greetings! Check out the chat rules. Do you agree with them?\n"
            "https://teletype.in/@coiners/Um4d1JbBAgD."
        ),
        reply_markup=accept_rules_keyboard(),
    )


async def accept_rules(message: types.Message, state: FSMContext):
    if message.text in ("I accept", "Принимаю", "ვღებულობ"):
        await recreate_user(message.from_user.id)
        invite_link = await create_invite_link(message)
        await message.answer(
            text=_(
                "Excellent!\nHere is the link to join the group: {invite_link}\n\n"
                "You can always get acquainted with our referral system, write to the admin, or request "
                "a referral link to invite a friend and earn yourself a rating 😎"
            ).format(invite_link=invite_link),
            reply_markup=main_keyboard(),
        )
        await state.finish()
        await state.reset_state()
    elif message.text in ("Do not Accept", "Не принимаю", "არ ვღებულობ"):
        await message.answer(
            text=_(
                "It's a pity! 😓\nWithout accepting the terms, we will "
                "not be able to accept you to join the community!"
            ),
            reply_markup=accept_rules_keyboard(),
        )
    elif message.text == "/start":
        await state.finish()
        await start(message)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(set_lang, content_types=["text"], state=FormAcceptRules.set_lang)
    dp.register_message_handler(accept_rules, content_types=["text"], state=FormAcceptRules.accept_rules)

    dp.register_message_handler(
        start,
        Text(equals=["Join the group 🤑", "Присоединиться к группе 🤑", "ჯგუფში გაწევრიანება 🤑"]),
    )
