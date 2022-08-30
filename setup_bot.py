from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from connectors.coin_api import CoinApiClient
from connectors.users_api import UsersApiClient

from settings import COIN_API_SERVICE, SERVICE_USERS_API_BASE_URL, TOKEN


class CryptoAlfredBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_api_client = UsersApiClient.create(base_url=SERVICE_USERS_API_BASE_URL)
        self.coin_api_client = CoinApiClient.create(**COIN_API_SERVICE)


storage = MemoryStorage()
bot = CryptoAlfredBot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
