from typing import Any, Optional, Tuple

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from connectors.coin_api import CoinApiClient
from connectors.users_api import UsersApiClient

from settings import COIN_API_SERVICE, I18N_DOMAIN, LOCALES_DIR, SERVICE_USERS_API_BASE_URL, TOKEN


class CryptoAlfredBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_api_client = UsersApiClient.create(base_url=SERVICE_USERS_API_BASE_URL)
        self.coin_api_client = CoinApiClient.create(**COIN_API_SERVICE)


storage = MemoryStorage()
bot = CryptoAlfredBot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        if action == "pre_process_message":
            user = await bot.users_api_client.get_user(user_id=args[0].from_user.id)

            if user.get("detail"):  # not found
                deleted_user = await bot.users_api_client.get_deleted_user(user_id=args[0].from_user.id)

                if deleted_user.get("detail"):  # not found
                    deleted_user = await bot.users_api_client.create_user(
                        user_id=args[0].from_user.id,
                        chat_id=args[0].chat.id,
                        username=args[0].from_user.username,
                        first_name=args[0].from_user.first_name,
                        last_name=args[0].from_user.last_name,
                        lang="en",
                    )

                elif deleted_user.get("join_to_group_count") == 0:
                    if args[0].text == "Русский 🇷🇺":
                        deleted_user = await bot.users_api_client.update_lang(
                            user_id=args[0].from_user.id, lang="ru"
                        )
                    elif args[0].text == "English 🇬🇧":
                        deleted_user = await bot.users_api_client.update_lang(
                            user_id=args[0].from_user.id, lang="en"
                        )
                    elif args[0].text == "ქართული 🇬🇪":
                        deleted_user = await bot.users_api_client.update_lang(
                            user_id=args[0].from_user.id, lang="ka"
                        )

                return deleted_user.get("lang")
            return user.get("lang")


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n


i18n = setup_middleware(dp)
_ = i18n.gettext
