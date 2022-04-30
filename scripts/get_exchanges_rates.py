import logging
from envparse import Env

from scripts.models import ExhangeData
from scripts.settings import COINAPI_SETTINGS
import requests

env = Env()

logger = logging.getLogger(__name__)


class CoinApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def default_headers(self):
        return {
            "X-CoinAPI-Key": f"{self.api_key}"
        }

    def proccess_response(self, resp):
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"status code in resp is not successful: {resp.status_code}")

    def get_exchange_rates(self):
        url = f"{self.base_url}/v1/assets"
        resp = requests.get(url=url, headers=self.default_headers())
        resp = self.proccess_response(resp)
        for rate in resp:
            current_rate = ExhangeData(**rate)
            if current_rate.asset_id == "BTC":
                return current_rate


if __name__ == "__main__":
    coin_api_client = CoinApiClient(**COINAPI_SETTINGS)
    print(coin_api_client.get_exchange_rates())
