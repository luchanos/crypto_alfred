from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from clients.coin_api_client import get_exchange_rates
from clients.tg_client import check_permissions, get_referral_link
from keyboards.main_keyboard import main_keyboard
from keyboards.write_to_admin_keyboard import write_to_admin_keyboard


async def get_referal_system_help(message: types.Message):
    await message.answer("Here is our referral system:#######", reply_markup=main_keyboard)


async def write_to_admin(message: types.Message):
    # await FormWriteToAdmin.write_message_to_admin.set()
    await message.answer("What do you want to write?", reply_markup=write_to_admin_keyboard)


# async def write_to_admin_handler(message: types.Message, state: FSMContext):
#     if message.text == "Отмена":
#         await message.answer("Ок, возврат в главное меню", reply_markup=main_keyboard)
#         await state.finish()
#     else:
#         await bot.send_message(
#             chat_id=ADMIN_CHAT_ID,
#             text=f"Пользователь @{message.from_user.username} оставил обращение:\n\n«{message.text.strip()}»"
#         )
#         await message.answer("Спасибо. Ваше обращение зарегистрировано!", reply_markup=main_keyboard)
#         await state.finish()


async def back_to_main(message: types.Message):
    await message.answer("Ok, back to main menu", reply_markup=main_keyboard)


@check_permissions
async def give_referral_link(message: types.Message, **kwargs):
    link = await get_referral_link(message)
    await message.answer(
        f"Here is your referral link:\n{link}\nSend it to your friend 😎", reply_markup=main_keyboard
    )


async def exchange_rates(message: types.Message):
    msg = "\n".join(
        f"{rate['name']} ({rate['asset_id']}): {'{:.4f}'.format(rate['price_usd'])}$"
        for rate in await get_exchange_rates()
    )
    await message.answer(msg, reply_markup=main_keyboard)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_referal_system_help, Text(equals="Reference ❓"))
    dp.register_message_handler(write_to_admin, Text(equals="Write to admin ✍️"))
    dp.register_message_handler(give_referral_link, Text(equals="Referral link 🤝"))
    dp.register_message_handler(back_to_main, Text(equals="Cancel 🔙"))
    dp.register_message_handler(exchange_rates, Text(equals="Exchange rates 💲"))
    # dp.register_message_handler(
    #     write_to_admin_handler, content_types=["text"], state=FormWriteToAdmin.write_message_to_admin
    # )
