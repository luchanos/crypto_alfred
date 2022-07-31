from envparse import Env

from raw_telegram_client import TelegramClientRaw
from scripts.get_exchanges_rates import CoinApiClient
from scripts.settings import COINAPI_SETTINGS


env = Env()
BASE_TG_URL = env.str("TELEGRAM_BASE_URL", default="https://api.telegram.org")
TOKEN = env.str("TOKEN")
CURRENCIES = ["BTC", "ETH"]
CURRENCY_RATE_MAPPER = {"BTC": "🌐", "ETH": "🔹"}


def make_rates_msg(rates):
    msg = f"**На сегодня курсы валют такие:**\n"
    for rate in rates.rates:
        formatted_price = f"{rate.price_usd:.4f}".replace(".", ",")
        msg += (
            f"\n{CURRENCY_RATE_MAPPER[rate.asset_id]} *{rate.name} \\({rate.asset_id}\\):" f"* {formatted_price} $"
        )
    return msg


if __name__ == "__main__":
    tg_client = TelegramClientRaw(base_url=BASE_TG_URL, token=TOKEN)
    coin_api_client = CoinApiClient(**COINAPI_SETTINGS)
    exchange_rates = coin_api_client.get_exchange_rates(CURRENCIES)
    tg_client.send_message(chat_id=-1001654253357, message=make_rates_msg(exchange_rates))
