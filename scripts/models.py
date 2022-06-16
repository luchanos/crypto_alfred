from pydantic import BaseModel
from pydantic.typing import Optional


class ExhangeData(BaseModel):
    asset_id: str
    name: str
    price_usd: Optional[float]


class ExchangeRateList(BaseModel):
    rates: list[ExhangeData]
