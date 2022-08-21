from settings import DEFAULT_EXCHANGE_RATES
from setup_bot import bot


async def get_exchange_rates():
    return await bot.coin_api_client.get_exchange_rates(DEFAULT_EXCHANGE_RATES)
