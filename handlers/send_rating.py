from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from clients.users_api_client import get_user, send_rating_to_user
from keyboards import confirmation_send_rating_keyboard, main_keyboard, stop_send_rating_keyboard
from setup_bot import _


class FormSendRating(StatesGroup):
    wallet = State()
    amount = State()
    confirm = State()


async def my_wallet(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(
            text=_("Your wallet: {wallet}\nYour rating: {rating}").format(
                wallet=message.from_user.id, rating=user.get("total_rating")
            )
        )


async def send_rating(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await FormSendRating.wallet.set()
        await message.answer(
            text=_("Enter the recipient's wallet number"), reply_markup=stop_send_rating_keyboard()
        )


async def process_wallet(message: Message, state: FSMContext):
    if message.text in ("Cancel ❌", "Отмена ❌", "გაუქმება ❌"):
        await state.finish()
        await message.answer(text=_("Ok, back to main menu"), reply_markup=main_keyboard())
    elif not message.text.isdigit():
        await message.answer(
            text=_("The wallet address can only be a numbers! Enter wallet number again"),
            reply_markup=stop_send_rating_keyboard(),
        )
    else:
        to_user = await get_user(message.text)
        from_user = await get_user(message.from_user.id)
        if to_user.get("user_id"):
            async with state.proxy() as data:
                data["wallet"] = message.text

            await FormSendRating.next()
            await message.answer(
                text=_("Enter the rating amount.\nAvailable: {rating}").format(
                    rating=from_user.get("total_rating")
                ),
                reply_markup=stop_send_rating_keyboard(),
            )
        else:
            await message.answer(
                text=_("Wallet not found! Enter the correct wallet address."),
                reply_markup=stop_send_rating_keyboard(),
            )


async def process_rating_value(message: Message, state: FSMContext):
    if message.text in ("Cancel ❌", "Отмена ❌", "გაუქმება ❌"):
        await state.finish()
        await message.answer(text=_("Ok, back to main menu"), reply_markup=main_keyboard())
    elif not message.text.isdigit():
        await message.answer(
            text=_("The number of ratings can only be a number! Enter rating amount again."),
            reply_markup=stop_send_rating_keyboard(),
        )
    elif int(message.text) < 1:
        await message.answer(text=_("Enter an amount no less than 1"), reply_markup=stop_send_rating_keyboard())
    else:
        async with state.proxy() as data:
            data["amount"] = message.text

        await FormSendRating.next()
        await message.answer(
            text=_("Rating: {rating}\nRecipient: {wallet}\n\nSend?").format(
                rating=data["amount"], wallet=data["wallet"]
            ),
            reply_markup=confirmation_send_rating_keyboard(),
        )


async def confirm_send(message: Message, state: FSMContext):
    if message.text in ("Yes", "Да", "დიახ"):
        current_state = await state.get_state()
        if current_state is None:
            return

        from_username = message.from_user.username

        async with state.proxy() as data:
            from_user = message.from_user.id
            to_user = data["wallet"]
            amount = data["amount"]
            res = await send_rating_to_user(from_user, to_user, amount)

            if res.get("Success"):
                await message.answer(text=_("Success!"), reply_markup=main_keyboard())
                to_user = await get_user(to_user)
                await message.bot.send_message(
                    chat_id=to_user.get("user_id"),
                    text=_(
                        "You have received {amount} rating points {from_username}", locale=to_user.get("lang")
                    ).format(amount=amount, from_username=f"\n@{from_username}" if from_username else ""),
                )

            elif res.get("detail") == f"User {from_user} has no sufficient rating on deposit":
                await message.answer(
                    text=_("You don't have enough rating points for transfer!"), reply_markup=main_keyboard()
                )

        await state.finish()

    elif message.text in ("No", "Нет", "არა"):
        await state.finish()
        await message.answer(text=_("Ok!"), reply_markup=main_keyboard())


def register_handlers_send_rating(dp: Dispatcher):
    dp.register_message_handler(my_wallet, Text(equals=["My wallet 💰", "Мой кошелек 💰", "ჩემი საფულე 💰"]))
    dp.register_message_handler(send_rating, Text(equals=["Send 💸", "Отправить 💸", "გადარიცხვა 💸"]))

    dp.register_message_handler(process_wallet, content_types=["text"], state=FormSendRating.wallet)
    dp.register_message_handler(process_rating_value, content_types=["text"], state=FormSendRating.amount)
    dp.register_message_handler(confirm_send, content_types=["text"], state=FormSendRating.confirm)
