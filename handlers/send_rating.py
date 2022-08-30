from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from clients.users_api_client import get_user, send_rating_to_user
from keyboards import confirmation_send_rating_keyboard, main_keyboard, stop_send_rating_keyboard
from setup_bot import dp


class FormSendRating(StatesGroup):
    wallet = State()
    amount = State()


async def my_wallet(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(text=f"Your wallet: {message.from_user.id}\nYour rating: {user.get('total_rating')}")


async def send_rating(message: Message):
    await FormSendRating.wallet.set()
    await message.answer(text="Enter the recipient's wallet number", reply_markup=stop_send_rating_keyboard)


async def process_wallet_invalid(message: Message):
    await message.answer(
        text="The wallet number can only be a number! Enter wallet number again",
        reply_markup=stop_send_rating_keyboard,
    )


async def process_wallet(message: Message, state: FSMContext):
    to_user = await get_user(message.text)
    from_user = await get_user(message.from_user.id)
    if to_user.get("user_id"):
        async with state.proxy() as data:
            data["wallet"] = message.text

        await FormSendRating.next()
        await message.answer(
            text=f"Enter the rating amount.\nAvailable: {from_user.get('total_rating')}",
            reply_markup=stop_send_rating_keyboard,
        )
    else:
        await FormSendRating.wallet.set()
        await message.answer(
            text="Wallet not found! Enter the correct wallet. ", reply_markup=stop_send_rating_keyboard
        )


async def process_rating_value_invalid_zero(message: Message):
    await message.answer(text="Enter an amount no less than 1", reply_markup=stop_send_rating_keyboard)


async def process_rating_value_invalid(message: Message):
    await message.answer(
        text="The number of ratings can only be a number! Enter rating amount again. ",
        reply_markup=stop_send_rating_keyboard,
    )


async def process_rating_value(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["amount"] = message.text

    await message.answer(
        text=f"Rating: {data['amount']}\nRecipient: {data['wallet']}\n\nSend?",
        reply_markup=confirmation_send_rating_keyboard,
    )


@dp.message_handler(state="*", commands="Yes")
async def sure_send(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    async with state.proxy() as data:
        from_user = message.from_user.id
        to_user = data["wallet"]
        amount = data["amount"]
        res = await send_rating_to_user(from_user, to_user, amount)

        if res.get("Success"):
            await message.answer(text=f"Success!", reply_markup=main_keyboard)
            await message.bot.send_message(chat_id=to_user, text=f"You have received {amount} rating points")

        elif res.get("detail") == f"User {from_user} has no sufficient rating on deposit":
            await message.answer(text="You don't have enough rating for transfer!", reply_markup=main_keyboard)

        elif res.get("detail") == f"User with user_id {to_user} not found":
            await message.answer(text="Wallet number not found!", reply_markup=main_keyboard)

    await state.finish()


@dp.message_handler(state="*", commands="No")
async def not_sure_send(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer(text="Ok!", reply_markup=main_keyboard)


@dp.message_handler(state="*", commands="Cancel ❌")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer(text="Ok, back to main menu", reply_markup=main_keyboard)


def register_handlers_send_rating(dp: Dispatcher):
    dp.register_message_handler(my_wallet, Text(equals=f"My wallet 💰"))

    dp.register_message_handler(send_rating, Text(equals=f"Share rating 💸"))

    dp.register_message_handler(cancel_handler, Text(equals="Cancel ❌", ignore_case=True), state="*")
    dp.register_message_handler(sure_send, Text(equals="Yes", ignore_case=True), state="*")
    dp.register_message_handler(not_sure_send, Text(equals="No", ignore_case=True), state="*")

    dp.register_message_handler(
        process_wallet_invalid, lambda message: not message.text.isdigit(), state=FormSendRating.wallet
    )

    dp.register_message_handler(
        process_wallet, lambda message: message.text.isdigit(), state=FormSendRating.wallet
    )

    dp.register_message_handler(
        process_rating_value_invalid, lambda message: not message.text.isdigit(), state=FormSendRating.amount
    )

    dp.register_message_handler(
        process_rating_value_invalid_zero, lambda message: int(message.text) < 1, state=FormSendRating.amount
    )

    dp.register_message_handler(
        process_rating_value, lambda message: message.text.isdigit(), state=FormSendRating.amount
    )
