from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from connectors.users_api import UsersApiClient

from settings import SERVICE_USERS_API_BASE_URL, TOKEN


class CryptoAlfredBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_api_client = UsersApiClient.create(base_url=SERVICE_USERS_API_BASE_URL)


storage = MemoryStorage()
bot = CryptoAlfredBot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
