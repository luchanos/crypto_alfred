from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from clients.tg_client import get_referral_link
from clients.users_api_client import get_user, update_lang
from keyboards import set_lang_keyboard
from keyboards.main_keyboard import main_keyboard
from keyboards.write_to_admin_keyboard import write_to_admin_keyboard
from setup_bot import _


class FormChangeLang(StatesGroup):
    set_lang = State()


class FormWriteToAdmin(StatesGroup):
    message = State()


async def write_to_admin(message: types.Message):
    await FormWriteToAdmin.message.set()
    await message.answer(_("What do you want to write?"), reply_markup=write_to_admin_keyboard())


async def message_to_admin_handler(message: types.Message, state: FSMContext):
    if message.text in ("Cancel 🔙", "Отмена 🔙", "გაუქმება 🔙"):
        await message.answer(_("Ok, back to main menu"), reply_markup=main_keyboard())
        await state.finish()
    else:
        await message.answer(_("Ваше сообщение зарегистрировано!"), reply_markup=main_keyboard())
        await state.finish()


async def change_language(message: types.Message):
    await FormChangeLang.set_lang.set()
    await message.answer(text=_("Choose language"), reply_markup=set_lang_keyboard())


async def set_lang(message: types.Message, state: FSMContext):
    if message.text == "Русский 🇷🇺":
        await update_lang(user_id=message.from_user.id, lang="ru")
        await message.answer("Готово!", reply_markup=main_keyboard(locale="ru"))
        await state.finish()
    elif message.text == "English 🇬🇧":
        await update_lang(user_id=message.from_user.id, lang="en")
        await message.answer("Complete!", reply_markup=main_keyboard(locale="en"))
        await state.finish()
    elif message.text == "ქართული 🇬🇪":
        await update_lang(user_id=message.from_user.id, lang="ka")
        await message.answer("ცვლილება წარმატებულია", reply_markup=main_keyboard(locale="ka"))
        await state.finish()


async def give_referral_link(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        link = await get_referral_link(message)
        if link:
            await message.answer(
                _("Here is your referral link:\n{link}\nSend it to your friend 😎").format(link=link),
                reply_markup=main_keyboard(),
            )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        write_to_admin,
        Text(equals=["Write to administration ✍️", "Написать администратору ✍️", "წერილი ადმინისტრაციას ✍️"]),
    )
    dp.register_message_handler(message_to_admin_handler, content_types=["text"], state=FormWriteToAdmin.message)

    dp.register_message_handler(change_language, Text(equals=["Language 🌐", "Язык 🌐", "ენა 🌐"]))
    dp.register_message_handler(set_lang, content_types=["text"], state=FormChangeLang.set_lang)

    dp.register_message_handler(
        give_referral_link, Text(equals=["Referral link 🤝", "Реферальная ссылка 🤝", "რეფერალური ბმული 🤝"])
    )
