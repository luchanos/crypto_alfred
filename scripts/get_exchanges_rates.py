import logging
from typing import Optional

from envparse import Env

from scripts.models import ExhangeData, ExchangeRateList
import requests

env = Env()

logger = logging.getLogger(__name__)


class CoinApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def default_headers(self) -> dict:
        return {
            "X-CoinAPI-Key": f"{self.api_key}"
        }

    @staticmethod
    def proccess_response(resp) -> dict:
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(f"status code in resp is not successful: {resp.status_code}")

    def get_exchange_rates(self, currency_list: Optional[list[str]] = None) -> ExchangeRateList:
        url = f"{self.base_url}/v1/assets"
        resp = requests.get(url=url, headers=self.default_headers())
        resp = self.proccess_response(resp)
        rates = []
        for rate in resp:
            for currency in currency_list:
                current_rate = ExhangeData(**rate)
                if current_rate.asset_id == currency:
                    rates.append(current_rate)
        return ExchangeRateList(rates=rates)
