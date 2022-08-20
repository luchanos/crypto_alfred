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
        await message.answer(
            text=f"Твой кошелек: {message.from_user.id}\nТвой рейтинг: {user.get('total_rating')}"
        )


async def send_rating(message: Message):
    await FormSendRating.wallet.set()
    await message.answer(text="Введите номер кошелька получателя", reply_markup=stop_send_rating_keyboard)


async def process_wallet_invalid(message: Message):
    await message.answer(
        text="Номер кошелька может быть только числом ! Введите номер кошелька еще раз",
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
            text=f"Введите количество рейтинга.\nДоступно: {from_user.get('total_rating')}",
            reply_markup=stop_send_rating_keyboard,
        )
    else:
        await FormSendRating.wallet.set()
        await message.answer(
            text="Кошелек не найден! Введите правильный кошелек", reply_markup=stop_send_rating_keyboard
        )


async def process_rating_value_invalid_zero(message: Message):
    await message.answer(text="Введите сумму не меньше 1", reply_markup=stop_send_rating_keyboard)


async def process_rating_value_invalid(message: Message):
    await message.answer(
        text="Количество рейтинга может быть только числом ! Введите сумму рейтинга еще раз",
        reply_markup=stop_send_rating_keyboard,
    )


async def process_rating_value(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["amount"] = message.text

    await message.answer(
        text=f"Рейтинг: {data['amount']}\nПолучатель: {data['wallet']}\n\nОтправить?",
        reply_markup=confirmation_send_rating_keyboard,
    )


@dp.message_handler(state="*", commands="Да")
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
            await message.answer(text=f"Успешно!", reply_markup=main_keyboard)
            await message.bot.send_message(chat_id=to_user, text=f"Вам перевели {amount} очков рейтинга")
        elif res.get("detail") == f"User {from_user} has no sufficient rating on deposit":
            await message.answer(text="У вас не достаточно рейтинга для перевода!", reply_markup=main_keyboard)
        elif res.get("detail") == f"User with user_id {to_user} not found":
            await message.answer(text="Номер кошелька не найден!!", reply_markup=main_keyboard)

    await state.finish()


@dp.message_handler(state="*", commands="Нет")
async def not_sure_send(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer(text="Хорошо!", reply_markup=main_keyboard)


@dp.message_handler(state="*", commands="Отмена ❌")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer(text="Ок, возврат в главное меню", reply_markup=main_keyboard)


def register_handlers_send_rating(dp: Dispatcher):
    dp.register_message_handler(my_wallet, Text(equals=f"Мой кошелек 💰"))

    dp.register_message_handler(send_rating, Text(equals=f"Поделиться рейтингом 💸"))

    dp.register_message_handler(cancel_handler, Text(equals="Отмена ❌", ignore_case=True), state="*")
    dp.register_message_handler(sure_send, Text(equals="Да", ignore_case=True), state="*")
    dp.register_message_handler(not_sure_send, Text(equals="Нет", ignore_case=True), state="*")

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
